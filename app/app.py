"""Flask web application reproducing the thesis experiment.

Pages
  /                     overview + thesis summary
  /detect/spam          Spam e-mail detection (Spambase)
  /detect/phishing      Phishing website detection
  /results              side-by-side thesis vs computed values
  /params               Table 4-4 parameters
  /experiments          all experiments (convergence / ROC / metrics / CM)
"""
from __future__ import annotations

import threading
import traceback
import uuid

import numpy as np
from flask import Flask, jsonify, render_template, request

from engine import (PARAMS_TABLE, THESIS, feature_ranges, load_dataset,
                    predict_raw, predict_sample, run_experiment, sample_batch)
from feature_meta import FEATURE_NAMES, PHISHING_FEATURES
from text_analyzer import explain_spambase, extract_spambase_features
from url_analyzer import feature_vector

app = Flask(__name__)

# in-memory job registry: id -> {status, progress, result, error}
JOBS: dict[str, dict] = {}
LOCK = threading.Lock()


# --------------------------------------------------------------------------- #
#  Routes — pages                                                             #
# --------------------------------------------------------------------------- #
@app.route("/")
def index():
    stats = {}
    for key in ("spambase", "phishing"):
        X, y, _ = load_dataset(key)
        stats[key] = {
            "samples": int(X.shape[0]),
            "features": int(X.shape[1]),
            "class_counts": {int(k): int(v)
                             for k, v in zip(*np.unique(y, return_counts=True))},
        }
    return render_template("index.html", thesis=THESIS, stats=stats)


@app.route("/detect/<key>")
def detect(key):
    if key not in THESIS:
        return "Unknown dataset", 404
    cfg = THESIS[key]
    X, y, _ = load_dataset(key)
    return render_template("detect.html", key=key, cfg=cfg,
                           n_features=X.shape[1])


@app.route("/results")
def results():
    return render_template("results.html", thesis=THESIS)


@app.route("/params")
def params():
    return render_template("params.html", params=PARAMS_TABLE, thesis=THESIS)


@app.route("/experiments")
def experiments():
    return render_template("experiments.html", thesis=THESIS)


@app.route("/methodology")
def methodology():
    return render_template("methodology.html", thesis=THESIS)


# --------------------------------------------------------------------------- #
#  API — run the experiment asynchronously                                    #
# --------------------------------------------------------------------------- #
@app.post("/api/run")
def api_run():
    data = request.get_json(force=True, silent=True) or {}
    key = data.get("dataset", "spambase")
    if key not in THESIS:
        return jsonify({"error": "unknown dataset"}), 400

    job_id = uuid.uuid4().hex[:12]
    with LOCK:
        JOBS[job_id] = {"status": "running", "progress": 0, "result": None,
                        "error": None}

    def worker():
        try:
            def progress(done, total, cost):
                with LOCK:
                    JOBS[job_id]["progress"] = round(100 * done / total, 1)
                    JOBS[job_id]["cost"] = cost

            res = run_experiment(
                key,
                n_pop=int(data.get("n_pop", 20)),
                max_it=int(data.get("max_it", 20)),
                desired=int(data.get("desired") or THESIS[key]["n_selected"]),
                test_size=float(data.get("test_size", 0.2)),
                seed=int(data.get("seed", 0)),
                progress=progress,
            )
            with LOCK:
                JOBS[job_id]["result"] = res
                JOBS[job_id]["status"] = "done"
                JOBS[job_id]["progress"] = 100
        except Exception:  # surface the traceback to the client
            with LOCK:
                JOBS[job_id]["status"] = "error"
                JOBS[job_id]["error"] = traceback.format_exc()

    threading.Thread(target=worker, daemon=True).start()
    return jsonify({"job_id": job_id})


@app.get("/api/job/<job_id>")
def api_job(job_id):
    with LOCK:
        job = JOBS.get(job_id)
        if not job:
            return jsonify({"error": "unknown job"}), 404
        return jsonify(job)


# --------------------------------------------------------------------------- #
#  API — single sample classification (fake / real)                           #
# --------------------------------------------------------------------------- #
@app.post("/api/predict")
def api_predict():
    data = request.get_json(force=True, silent=True) or {}
    key = data.get("dataset", "spambase")
    if key not in THESIS:
        return jsonify({"error": "unknown dataset"}), 400
    values = data.get("values")
    if values is not None:
        values = [float(v) for v in values]
    res = predict_sample(key, values=values, seed=int(data.get("seed", 0)))
    return jsonify(res)


@app.post("/api/samples")
def api_samples():
    data = request.get_json(force=True, silent=True) or {}
    key = data.get("dataset", "spambase")
    if key not in THESIS:
        return jsonify({"error": "unknown dataset"}), 400
    return jsonify(sample_batch(key, n=int(data.get("n", 8)),
                                seed=int(data.get("seed", 0))))


@app.post("/api/analyze_text")
def api_analyze_text():
    """Paste a real e-mail body -> Spambase features -> verdict."""
    data = request.get_json(force=True, silent=True) or {}
    text = data.get("text", "")
    if not text.strip():
        return jsonify({"error": "النص فارغ"}), 400
    vec = extract_spambase_features(text)
    verdict = predict_raw("spambase", vec, top_k=8)
    explain = explain_spambase(text)
    return jsonify({"verdict": verdict, "explain": explain, "vector": vec})


@app.post("/api/analyze_url")
def api_analyze_url():
    """Enter a URL -> Phishing features -> verdict."""
    data = request.get_json(force=True, silent=True) or {}
    url = (data.get("url") or "").strip()
    if not url:
        return jsonify({"error": "الرابط فارغ"}), 400
    vec, info = feature_vector(url)
    verdict = predict_raw("phishing", vec, top_k=8)
    order = [n for n, _, _ in PHISHING_FEATURES]
    labels = {n: lbl for n, lbl, _ in PHISHING_FEATURES}
    legends = {n: leg for n, _, leg in PHISHING_FEATURES}
    table = [{
        "name": n,
        "label": labels[n],
        "value": int(info["features"][n]),
        "meaning": legends[n].get(int(info["features"][n]), ""),
    } for n in order]
    return jsonify({"verdict": verdict, "meta": info["meta"],
                    "signals": info["signals"], "table": table,
                    "vector": vec})


@app.post("/api/predict_manual")
def api_predict_manual():
    """Classify a hand-entered feature vector."""
    data = request.get_json(force=True, silent=True) or {}
    key = data.get("dataset", "spambase")
    if key not in THESIS:
        return jsonify({"error": "unknown dataset"}), 400
    try:
        values = [float(v) for v in data.get("values", [])]
    except (TypeError, ValueError):
        return jsonify({"error": "قيم غير رقمية"}), 400
    if not values:
        return jsonify({"error": "لم تُدخل أي قيمة"}), 400
    try:
        res = predict_raw(key, values, top_k=8)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(res)


@app.get("/api/features/<key>")
def api_features(key):
    """Feature metadata so the manual-entry form can render itself."""
    if key not in THESIS:
        return jsonify({"error": "unknown dataset"}), 400
    lo, hi = feature_ranges(key)
    if key == "phishing":
        items = [{
            "name": n, "label": lbl, "values": [
                {"value": v, "meaning": leg[v]} for v in sorted(leg, reverse=True)
            ],
        } for n, lbl, leg in PHISHING_FEATURES]
    else:
        names = FEATURE_NAMES[key]
        items = [{"name": n, "label": n,
                  "values": [{"value": None, "meaning": "قيمة عشرية"},
                             {"value": 0, "meaning": "صفر"}]}
                 for n in names]
    return jsonify({"items": items,
                    "ranges": {"min": lo.tolist(), "max": hi.tolist()},
                    "defaults": ((lo + hi) / 2).tolist()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=12000, debug=False, threaded=True)
