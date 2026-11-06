"""Hybrid PSO-GA feature selection with a Random Forest classifier.

Direct re-implementation of the MATLAB sources shipped with the thesis:

    main.m                      - full pipeline for the Spambase dataset
    GA_PSO_feature_selection.m  - PSO velocity update + GA crossover/mutation
    fitness_RF.m                - cost function (RF error + feature penalty)
    repair_solution.m           - force the chromosome to hold N selected genes
    plot_results.m              - final model, metrics, ROC, confusion matrix

Everything the thesis reports (values, curves, matrices) is produced here.
"""
from __future__ import annotations

from pathlib import Path
import time

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score,
                             roc_curve)
from sklearn.model_selection import train_test_split

from . import feature_meta

EPS = np.finfo(float).eps

# --------------------------------------------------------------------------- #
#  Values published in the thesis (verbatim)                                   #
# --------------------------------------------------------------------------- #
THESIS = {
    "spambase": {
        "title": "Spam Email Detection",
        "title_ar": "كشف البريد الإلكتروني المزيف",
        "dataset": "Spambase",
        "n_samples": 4601,
        "n_features": 57,
        "n_selected": 46,
        "pos_label": 1,
        "class_names": ["Ham (0)", "Spam (1)"],
        "accuracy": 96.79,
        "precision": 96.40,
        "recall": 97.89,
        "f1": 97.14,
        "auc": 0.988,
        "confusion_matrix": [[538, 20], [23, 339]],
        "cm_labels": ["Healthy email (class 0)", "Spam email (class 1)"],
    },
    "phishing": {
        "title": "Phishing Website Detection",
        "title_ar": "كشف المواقع المزيفة",
        "dataset": "Phishing Websites",
        "n_samples": 11055,
        "n_features": 30,
        "n_selected": 22,
        "pos_label": 1,
        "class_names": ["Legitimate (-1)", "Phishing (1)"],
        "accuracy": 98.20,
        "precision": 97.98,
        "recall": 98.80,
        "f1": 98.39,
        "auc": 0.996,
        "confusion_matrix": [[955, 25], [15, 1216]],
        "cm_labels": ["Legitimate (class -1)", "Phishing (class 1)"],
    },
}

# Table 4-4 of the thesis
PARAMS_TABLE = [
    ("Max Iteration", "MaxIt", "20",
     "Number of times the optimization process is executed"),
    ("Population Size", "nPop", "20",
     "Number of particles / chromosomes per iteration"),
    ("Inertia coefficient", "w", "0.7",
     "Balancing global and local search in PSO"),
    ("Cognitive learning coefficient", "c1", "1.5",
     "Effect of individual experience of each particle"),
    ("Social learning coefficient", "c2", "1.5",
     "Effect of best collective experience"),
    ("Crossover rate", "Pc", "0.8",
     "Probability of performing the combination operator"),
    ("Mutation rate", "Pm", "0.2",
     "Probability of random change of genes"),
    ("Parent selection", "-", "Roulette Wheel",
     "Select individuals based on fitness value"),
    ("Cross-validation", "K", "5",
     "K-Fold cross validation, prevent overfitting"),
    ("Crossover type", "-", "Single Point",
     "Generate new offspring from selected parents"),
    ("Mutation type", "-", "Bit Leap",
     "Randomly change the value of some genes"),
    ("Elitism", "-", "1 member",
     "Transfer the best solution unchanged"),
    ("Objective function", "-", "Combination Cost",
     "Minimize RF error and number of selected features"),
]

# --------------------------------------------------------------------------- #
#  Data paths — resolved relative to the package, so the app works when frozen #
# --------------------------------------------------------------------------- #
_PKG = Path(__file__).resolve().parent.parent        # .../thesis_app
_REPO = _PKG.parent.parent                           # .../project (dev checkout)


def _bundle_root() -> Path:
    """Root of the bundled assets: ``sys._MEIPASS`` inside a PyInstaller
    build, otherwise the package directory."""
    import sys

    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        return Path(meipass) / "thesis_app"
    return _PKG


_CANDIDATES = [
    _bundle_root() / "assets" / "data",              # bundled with the package
    _PKG / "assets" / "data",                        # source checkout
    _REPO / "extracted_zip" / "hussiandamghan",      # development tree
]

DATA_FILES = {"spambase": "spambase.xlsx", "phishing": "Data_phishing.xlsx"}

#: The MATLAB sources that ship with the thesis, in the order they run.
MATLAB_FILES = [
    "main.m",
    "GA_PSO_feature_selection.m",
    "fitness_RF.m",
    "repair_solution.m",
    "plot_results.m",
]

#: MATLAB artefacts that only MATLAB can open (``.fig``) plus the editor
#: backup of ``main.m``. They are shipped so the folder is complete, and the
#: application lists them rather than pretending they are missing.
MATLAB_EXTRA_FILES = [
    "main.asv",
    "curve.fig",
    "cm.fig",
    "roc.fig",
    "all.fig",
]

#: The nine result figures exported from the thesis, keyed by dataset.
FIGURES = {
    "spambase": [
        ("curve.jpg", "fig.curve_spam"),
        ("cm.jpg", "fig.cm_spam"),
        ("roc.jpg", "fig.roc_spam"),
        ("per.jpg", "fig.per_spam"),
        ("all.jpg", "fig.all_spam"),
    ],
    "phishing": [
        ("curvespam.jpg", "fig.curve_phish"),
        ("cmspam.jpg", "fig.cm_phish"),
        ("rocspam.jpg", "fig.roc_phish"),
        ("allspam.jpg", "fig.all_phish"),
    ],
}

_ASSET_DIRS = {
    "data": [_bundle_root() / "assets" / "data",
             _PKG / "assets" / "data",
             _REPO / "extracted_zip" / "hussiandamghan"],
    "matlab": [_bundle_root() / "assets",
               _bundle_root() / "assets" / "matlab",
               _PKG / "assets",
               _PKG / "assets" / "matlab",
               _REPO / "extracted_zip" / "hussiandamghan"],
    "figures": [_bundle_root() / "assets" / "figures",
                _PKG / "assets" / "figures",
                _REPO / "extracted_zip" / "hussiandamghan"],
}


def asset_path(kind: str, name: str) -> Path:
    """Locate one bundled asset by category (``data``/``matlab``/``figures``)."""
    for base in _ASSET_DIRS[kind]:
        p = base / name
        if p.exists():
            return p
    raise FileNotFoundError(f"asset {name!r} not found in any of "
                            + ", ".join(str(c) for c in _ASSET_DIRS[kind]))


def matlab_source(name: str) -> str:
    """Return one MATLAB source file verbatim, exactly as the thesis ships it."""
    return asset_path("matlab", name).read_text(encoding="utf-8",
                                                errors="replace")


def _data_path(key: str) -> Path:
    for base in _CANDIDATES:
        p = base / DATA_FILES[key]
        if p.exists():
            return p
    raise FileNotFoundError(
        f"dataset file for {key!r} not found; looked in "
        + ", ".join(str(c) for c in _CANDIDATES))


# --------------------------------------------------------------------------- #
#  Data loading                                                                #
# --------------------------------------------------------------------------- #
def load_raw(key: str):
    """Return (X_raw, y, feature_names) without normalization."""
    df = pd.read_excel(_data_path(key), header=None)
    X = df.iloc[:, :-1].to_numpy(float)
    y = df.iloc[:, -1].to_numpy(int)
    names = (feature_meta.FEATURE_NAMES.get(key)
             or [f"F{i + 1}" for i in range(X.shape[1])])
    return X, y, names


def feature_ranges(key: str):
    """(min, max) per feature over the whole dataset - the ranges main.m uses."""
    X, _, _ = load_raw(key)
    return X.min(0), X.max(0)


def normalize(X, lo, hi):
    """Min-Max normalization to [0,1], equation 3-1 of the thesis."""
    return (X - lo) / (hi - lo + EPS)


def load_dataset(key: str):
    """(X_normalized, y, feature_names). Matches main.m exactly."""
    X, y, names = load_raw(key)
    lo, hi = X.min(0), X.max(0)
    return normalize(X, lo, hi), y, names


# --------------------------------------------------------------------------- #
#  Deployed detector (trained on the full dataset, used for live prediction)   #
# --------------------------------------------------------------------------- #
_MODEL_CACHE: dict = {}


def get_model(key: str, seed: int = 0):
    ck = (key, seed)
    if ck not in _MODEL_CACHE:
        X, y, names = load_raw(key)
        lo, hi = X.min(0), X.max(0)
        rf = RandomForestClassifier(n_estimators=100, random_state=seed,
                                    n_jobs=-1)
        rf.fit(normalize(X, lo, hi), y)
        _MODEL_CACHE[ck] = {"rf": rf, "lo": lo, "hi": hi, "names": names}
    return _MODEL_CACHE[ck]


def _label_for(key: str, pred: int) -> str:
    cfg = THESIS[key]
    if key == "spambase":
        return "Spam / Fake" if pred == cfg["pos_label"] else "Ham / Real"
    return ("Phishing / Fake" if pred == cfg["pos_label"]
            else "Legitimate / Real")


def predict_raw(key, raw_values, seed=0, top_k=6):
    """Classify one sample given in *raw* (un-normalized) feature units."""
    cfg = THESIS[key]
    m = get_model(key, seed)
    lo, hi, names = m["lo"], m["hi"], m["names"]
    v = np.asarray(raw_values, float)
    if v.size != lo.size:
        raise ValueError(f"expected {lo.size} features, got {v.size}")
    v = np.clip(v, lo, hi)
    vn = normalize(v, lo, hi).reshape(1, -1)

    proba = m["rf"].predict_proba(vn)[0]
    classes = m["rf"].classes_.tolist()
    pred = int(classes[int(np.argmax(proba))])

    imp = m["rf"].feature_importances_
    order = np.argsort(imp)[::-1][:top_k]
    drivers = [{"feature": names[i], "importance": float(imp[i]),
                "value": float(v[i])} for i in order]

    return {
        "dataset_key": key,
        "prediction": pred,
        "prediction_label": _label_for(key, pred),
        "is_fake": pred == cfg["pos_label"],
        "confidence": float(proba.max()),
        "probabilities": proba.tolist(),
        "classes": classes,
        "class_names": cfg["class_names"],
        "drivers": drivers,
    }


# --------------------------------------------------------------------------- #
#  Core algorithm                                                              #
# --------------------------------------------------------------------------- #
def fitness(position, X, y, desired, n_estimators=50, seed=0):
    """fitness_RF.m - RF accuracy on the selected features plus a penalty on
    the number of selected features.  cost = (1-acc) + 0.01*penalty."""
    feats = np.flatnonzero(position)
    if feats.size == 0:
        return 1.0
    rf = RandomForestClassifier(n_estimators=n_estimators, random_state=seed,
                                n_jobs=-1)
    rf.fit(X[:, feats], y)
    acc = accuracy_score(y, rf.predict(X[:, feats]))
    penalty = abs(feats.size - desired) / desired
    return 1.0 - acc + 0.01 * penalty


def repair(position, desired, rng):
    """repair_solution.m - force exactly `desired` selected genes."""
    pos = position.copy()
    ones = np.flatnonzero(pos == 1)
    zeros = np.flatnonzero(pos == 0)
    if ones.size > desired:
        pos[rng.choice(ones, size=ones.size - desired, replace=False)] = 0
    elif ones.size < desired:
        pos[rng.choice(zeros, size=desired - ones.size, replace=False)] = 1
    return pos


def ga_pso(X, y, n_pop, max_it, desired, w=0.7, c1=1.5, c2=1.5,
           mutation_rate=0.2, seed=0, progress=None):
    """GA_PSO_feature_selection.m - PSO velocity/position update (sigmoid
    binarization), then GA crossover and bit-leap mutation, elite/global best."""
    rng = np.random.default_rng(seed)
    n_var = X.shape[1]

    pos = np.zeros((n_pop, n_var), dtype=int)
    vel = np.zeros((n_pop, n_var))
    cost = np.zeros(n_pop)
    pbest = np.zeros_like(pos)
    pbest_cost = np.full(n_pop, np.inf)

    for i in range(n_pop):
        idx = rng.choice(n_var, size=desired, replace=False)
        pos[i, idx] = 1
        cost[i] = fitness(pos[i], X, y, desired, seed=seed)
        pbest[i] = pos[i]
        pbest_cost[i] = cost[i]

    g = int(np.argmin(pbest_cost))
    gbest, gbest_cost = pbest[g].copy(), pbest_cost[g]

    curve = np.zeros(max_it)
    for it in range(max_it):
        for i in range(n_pop):
            r1, r2 = rng.random(n_var), rng.random(n_var)
            vel[i] = (w * vel[i] + c1 * r1 * (pbest[i] - pos[i])
                      + c2 * r2 * (gbest - pos[i]))
            sig = 1.0 / (1.0 + np.exp(-vel[i]))
            pos[i] = (sig > rng.random(n_var)).astype(int)
            pos[i] = repair(pos[i], desired, rng)
            cost[i] = fitness(pos[i], X, y, desired, seed=seed)
            if cost[i] < pbest_cost[i]:
                pbest_cost[i], pbest[i] = cost[i], pos[i]
                if pbest_cost[i] < gbest_cost:
                    gbest_cost, gbest = pbest_cost[i], pbest[i].copy()

        for _ in range(max(1, round(n_pop / 4))):          # GA crossover
            i1, i2 = rng.integers(n_pop), rng.integers(n_pop)
            alpha = rng.random()
            child = ((alpha * pos[i1] + (1 - alpha) * pos[i2]) > 0.5).astype(int)
            child = repair(child, desired, rng)
            child_cost = fitness(child, X, y, desired, seed=seed)
            worst = int(rng.integers(n_pop))
            if child_cost < cost[worst]:
                pos[worst], cost[worst] = child, child_cost
                pbest[worst], pbest_cost[worst] = child, child_cost

        for i in range(n_pop):                      # bit-leap mutation
            if rng.random() < mutation_rate:
                j = int(rng.integers(n_var))
                pos[i, j] = 1 - pos[i, j]
                pos[i] = repair(pos[i], desired, rng)
                cost[i] = fitness(pos[i], X, y, desired, seed=seed)

        curve[it] = gbest_cost
        if progress:
            progress(it + 1, max_it, float(gbest_cost))

    return gbest, gbest_cost, curve


def evaluate(Xtr, ytr, Xte, yte, selected, pos_label, seed=0):
    """plot_results.m - final Random Forest on the selected features plus every
    reported metric, curve and matrix."""
    rf = RandomForestClassifier(n_estimators=100, random_state=seed, n_jobs=-1)
    rf.fit(Xtr[:, selected], ytr)
    pred = rf.predict(Xte[:, selected])
    proba = rf.predict_proba(Xte[:, selected])[:, 1]

    fpr, tpr, _ = roc_curve((yte == pos_label).astype(int), proba)
    return {
        "accuracy": float(accuracy_score(yte, pred)),
        "precision": float(precision_score(yte, pred, pos_label=pos_label,
                                           zero_division=0)),
        "recall": float(recall_score(yte, pred, pos_label=pos_label,
                                     zero_division=0)),
        "f1": float(f1_score(yte, pred, pos_label=pos_label, zero_division=0)),
        "auc": float(roc_auc_score((yte == pos_label).astype(int), proba)),
        "confusion_matrix": confusion_matrix(yte, pred).tolist(),
        "train_accuracy": float(accuracy_score(ytr, rf.predict(Xtr[:, selected]))),
        "roc": {"fpr": fpr.tolist(), "tpr": tpr.tolist()},
        "n_test": int(yte.size),
        "n_train": int(ytr.size),
    }


def run_experiment(key, n_pop=20, max_it=20, desired=None, test_size=0.2,
                   seed=0, progress=None):
    """Full main.m pipeline for one dataset."""
    cfg = THESIS[key]
    desired = desired or cfg["n_selected"]
    X, y, names = load_dataset(key)

    t_start = time.perf_counter()
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=test_size, random_state=seed, stratify=y)

    gbest, gbest_cost, curve = ga_pso(
        Xtr, ytr, n_pop, max_it, desired, seed=seed, progress=progress)
    selected = np.flatnonzero(gbest)
    select_seconds = time.perf_counter() - t_start

    t_fit = time.perf_counter()
    res = evaluate(Xtr, ytr, Xte, yte, selected, cfg["pos_label"], seed=seed)
    fit_seconds = time.perf_counter() - t_fit

    # hypothesis 3 claims the subset cuts training time, so measure it;
    # hypotheses 1 and 2 claim it also raises accuracy, so measure that too
    t_all = time.perf_counter()
    baseline = evaluate(Xtr, ytr, Xte, yte, np.arange(X.shape[1]),
                        cfg["pos_label"], seed=seed)
    all_seconds = time.perf_counter() - t_all

    res.update({
        "dataset_key": key,
        "dataset": cfg["dataset"],
        "title": cfg["title"],
        "class_names": cfg["class_names"],
        "n_features": X.shape[1],
        "n_samples": X.shape[0],
        "n_selected": int(selected.size),
        "selected_features": [names[i] for i in selected],
        "convergence": curve.tolist(),
        "final_cost": float(gbest_cost),
        "select_seconds": select_seconds,
        "fit_seconds": fit_seconds,
        "all_features_seconds": all_seconds,
        "speedup": (all_seconds / fit_seconds) if fit_seconds else None,
        "baseline": {
            "accuracy": baseline["accuracy"],
            "precision": baseline["precision"],
            "recall": baseline["recall"],
            "f1": baseline["f1"],
            "auc": baseline["auc"],
        },
        "params": {"n_pop": n_pop, "max_it": max_it, "desired": desired,
                   "test_size": test_size, "seed": seed},
    })
    return res


def predict_sample(key, values=None, seed=0):
    """Classify one sample as fake/real.

    With ``values=None`` a random held-out test sample is drawn, so the reported
    confidence is realistic rather than a training-set overfit."""
    cfg = THESIS[key]
    X, y, names = load_dataset(key)

    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.2, random_state=seed, stratify=y)

    if values is None:
        rng = np.random.default_rng(seed)
        idx = int(rng.integers(Xte.shape[0]))
        v = Xte[idx].reshape(1, -1)
        true_label = int(yte[idx])
    else:
        v = np.asarray(values, float).reshape(1, -1)
        true_label = None

    rf = RandomForestClassifier(n_estimators=100, random_state=seed, n_jobs=-1)
    rf.fit(Xtr, ytr)
    pred = int(rf.predict(v)[0])
    proba = rf.predict_proba(v)[0]
    classes = rf.classes_.tolist()

    return {
        "dataset_key": key,
        "prediction": pred,
        "prediction_label": _label_for(key, pred),
        "confidence": float(proba.max()),
        "probabilities": proba.tolist(),
        "classes": classes,
        "class_names": cfg["class_names"],
        "true_label": true_label,
        "correct": (None if true_label is None else pred == true_label),
    }


def sample_batch(key, n=8, seed=0):
    """Classify several held-out samples for a prediction table."""
    cfg = THESIS[key]
    X, y, names = load_dataset(key)
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.2, random_state=seed, stratify=y)
    rf = RandomForestClassifier(n_estimators=100, random_state=seed, n_jobs=-1)
    rf.fit(Xtr, ytr)
    pred = rf.predict(Xte)
    proba = rf.predict_proba(Xte)

    rng = np.random.default_rng(seed)
    idx = rng.choice(Xte.shape[0], size=min(n, Xte.shape[0]), replace=False)

    rows = []
    for i in idx:
        p = int(pred[i])
        rows.append({
            "index": int(i),
            "true_label": int(yte[i]),
            "predicted": p,
            "label": _label_for(key, p),
            "confidence": float(proba[i].max()),
            "correct": bool(p == yte[i]),
        })
    return {"dataset_key": key, "rows": rows}
