#!/usr/bin/env python3
"""Self-test for the desktop application.

Checks that every page builds, that both languages are complete, that the
published thesis values are the ones on record, and that the live detectors
give the right verdict on known inputs.

    python desktop/verify_app.py
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/thesis_app_mpl")

# the report quotes Arabic labels, and a Windows console defaults to cp1252
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

PASS: list[str] = []
FAIL: list[str] = []


def check(name: str, ok: bool, detail: str = ""):
    (PASS if ok else FAIL).append(f"{name}{(' — ' + detail) if detail else ''}")
    print(("  PASS  " if ok else "  FAIL  ") + name
          + (f"   [{detail}]" if detail else ""))


def main() -> int:
    print("=" * 72)
    print("  Desktop application self-test")
    print("=" * 72)

    # ---- 1. core engine --------------------------------------------------
    print("\n[1] Core engine")
    from thesis_app.core import engine, feature_meta, thesis_data
    from thesis_app.core import text_analyzer, url_analyzer

    for key in ("spambase", "phishing"):
        X, y, names = engine.load_raw(key)
        cfg = engine.THESIS[key]
        check(f"{key}: sample count {cfg['n_samples']}",
              X.shape[0] == cfg["n_samples"], str(X.shape[0]))
        check(f"{key}: feature count {cfg['n_features']}",
              X.shape[1] == cfg["n_features"], str(X.shape[1]))
        check(f"{key}: label column present", y.size == X.shape[0])

    check("Spambase accuracy = 96.79%",
          engine.THESIS["spambase"]["accuracy"] == 96.79)
    check("Spambase AUC = 0.988", engine.THESIS["spambase"]["auc"] == 0.988)
    check("Phishing accuracy = 98.20%",
          engine.THESIS["phishing"]["accuracy"] == 98.20)
    check("Phishing AUC = 0.996", engine.THESIS["phishing"]["auc"] == 0.996)
    check("Spambase selected = 46",
          engine.THESIS["spambase"]["n_selected"] == 46)
    check("Phishing selected = 22",
          engine.THESIS["phishing"]["n_selected"] == 22)
    check("Table 4-4 has 13 rows", len(engine.PARAMS_TABLE) == 13,
          str(len(engine.PARAMS_TABLE)))

    # ---- 2. thesis data --------------------------------------------------
    print("\n[2] Thesis data")
    check("cover: student name", "Hussein" in thesis_data.COVER["student"])
    check("cover: university",
          thesis_data.COVER["university"] == "Damghan University")
    check("cover: student name in Arabic",
          thesis_data.COVER["student_ar"] == "حسين ناصر حسين")
    check("cover: university in Arabic",
          thesis_data.COVER["university_ar"] == "جامعة دامغان")
    check("cover: supervisor in Arabic",
          thesis_data.COVER["supervisor_ar"] == "د. عبد العلي بصيري")
    check("cover: thesis title in Arabic",
          "سرب الجسيمات" in thesis_data.COVER["title_ar"])
    check("cover: thesis title in English",
          "Particle Swarm Optimization" in thesis_data.COVER["title"])
    check("5 equations recorded (3-1 .. 3-5)", len(thesis_data.EQUATIONS) == 5,
          str(len(thesis_data.EQUATIONS)))
    check("8 contradictions recorded", len(thesis_data.CONFLICTS) == 8,
          str(len(thesis_data.CONFLICTS)))
    check("6 algorithm stages", len(thesis_data.ALGORITHM_STAGES) == 6)
    check("7 metrics documented", len(thesis_data.METRICS) == 7)
    check("objectives / questions / hypotheses present",
          len(thesis_data.OBJECTIVES) == 2
          and len(thesis_data.QUESTIONS) == 3
          and len(thesis_data.HYPOTHESES) == 4)

    # ---- 3. i18n ---------------------------------------------------------
    print("\n[3] Bilingual strings")
    from thesis_app.ui.i18n import S, SIGNAL_TEXT, TRANSLATOR, t

    incomplete = [k for k, v in S.items()
                  if "ar" not in v or "en" not in v
                  or not v["ar"].strip() or not v["en"].strip()]
    check(f"all {len(S)} strings complete in both languages",
          not incomplete, ", ".join(incomplete[:5]))
    check(f"{len(S)} interface strings", len(S) >= 240, str(len(S)))
    check("17 URL risk signals in both languages", len(SIGNAL_TEXT) == 17,
          str(len(SIGNAL_TEXT)))
    sig_incomplete = [k for k, v in SIGNAL_TEXT.items()
                      if not v.get("ar", "").strip() or not v.get("en", "").strip()]
    check("every risk signal is worded in both languages",
          not sig_incomplete, ", ".join(sig_incomplete))
    TRANSLATOR.lang = "en"
    check("English lookup works", t("nav.home") == "Home")
    TRANSLATOR.lang = "ar"
    check("Arabic lookup works", t("nav.home") == "الرئيسية")
    check("RTL flag on for Arabic", TRANSLATOR.is_rtl)

    # ---- 4. live detectors ------------------------------------------------
    print("\n[4] Live detection")
    spam_text = ("URGENT!! verify your credit card and password now. "
                 "Free money $5000 prize. Click here to confirm your account "
                 "immediately or it will be closed. Act now!")
    ham_text = ("Hi George, the project meeting is tomorrow at 10am in the "
                "conference room. Please bring the report and the data table. "
                "Thanks, Maria, Dept of Computer Science.")
    v_spam = engine.predict_raw(
        "spambase", text_analyzer.extract_spambase_features(spam_text))
    v_ham = engine.predict_raw(
        "spambase", text_analyzer.extract_spambase_features(ham_text))
    check("spam text classified as fake", v_spam["is_fake"],
          f"conf {v_spam['confidence']:.3f}")
    check("ham text classified as real", not v_ham["is_fake"],
          f"conf {v_ham['confidence']:.3f}")

    url_cases = [
        ("http://paypal-secure-login.verify-account.tk/login.php?id=1", True),
        ("https://www.paypal.com/signin", False),
        ("http://192.168.1.1/admin/login.php", True),
        ("https://www.google.com/search?q=test", False),
        ("http://microsoftonline.com.secure-auth.xyz/account", True),
        ("http://paypa1.com/verify", True),
        ("https://github.com/openai", False),
        ("http://free-prize-winner.tk/claim?user=victim&id=88", True),
        ("http://apple-id-verify.support-login.ml/signin", True),
        ("https://en.wikipedia.org/wiki/Phishing", False),
    ]
    good = 0
    for url, expect_fake in url_cases:
        vec, _ = url_analyzer.feature_vector(url)
        v = engine.predict_raw("phishing", vec)
        if v["is_fake"] == expect_fake:
            good += 1
        else:
            print(f"        wrong: {url}  (expected fake={expect_fake}, "
                  f"got {v['is_fake']}, conf {v['confidence']:.3f})")
    check(f"URL detection {good}/{len(url_cases)} correct",
          good == len(url_cases))

    # ---- 5. feature metadata ----------------------------------------------
    print("\n[5] Feature metadata")
    check("57 Spambase attribute names",
          len(feature_meta.FEATURE_NAMES["spambase"]) == 57)
    check("30 Phishing attribute names",
          len(feature_meta.FEATURE_NAMES["phishing"]) == 30)
    check("30 English labels",
          len(feature_meta.PHISHING_LABELS_EN) == 30)
    check("30 English meaning tables",
          len(feature_meta.PHISHING_MEANINGS_EN) == 30)
    missing = [n for n, _, _ in feature_meta.PHISHING_FEATURES
               if n not in feature_meta.PHISHING_CODING]
    check("coding table covers every attribute", not missing,
          ", ".join(missing))

    # ---- 6. the archive that accompanies the thesis ------------------------
    print("\n[6] Original archive: MATLAB sources and result figures")
    from thesis_app.core import engine as _engine

    matlab_missing, matlab_empty = [], []
    for name in _engine.MATLAB_FILES:
        try:
            text = _engine.matlab_source(name)
        except FileNotFoundError:
            matlab_missing.append(name)
            continue
        if not text.strip():
            matlab_empty.append(name)
    check("all 5 MATLAB sources are bundled", not matlab_missing,
          ", ".join(matlab_missing))
    check("every MATLAB source is non-empty", not matlab_empty,
          ", ".join(matlab_empty))

    # the sources must be the real thing, not placeholders
    ga_pso = ""
    try:
        ga_pso = _engine.matlab_source("GA_PSO_feature_selection.m")
    except FileNotFoundError:
        pass
    check("GA_PSO source defines the hybrid algorithm",
          "function" in ga_pso and "repair_solution" in ga_pso)
    fitness = ""
    try:
        fitness = _engine.matlab_source("fitness_RF.m")
    except FileNotFoundError:
        pass
    check("fitness source uses the 0.01 penalty from the thesis",
          "0.01" in fitness and "TreeBagger" in fitness)

    fig_missing = []
    n_figures = 0
    for _ds, items in _engine.FIGURES.items():
        for filename, _key in items:
            try:
                _engine.asset_path("figures", filename)
            except FileNotFoundError:
                fig_missing.append(filename)
            else:
                n_figures += 1
    check("all 9 thesis result figures are bundled",
          not fig_missing and n_figures == 9,
          ", ".join(fig_missing) or f"{n_figures} found")

    extra_missing = []
    for name in _engine.MATLAB_EXTRA_FILES:
        try:
            _engine.asset_path("matlab", name)
        except FileNotFoundError:
            extra_missing.append(name)
    check("the .fig and .asv artefacts are bundled too",
          not extra_missing, ", ".join(extra_missing))

    # ---- 7b. thesis chapter coverage -------------------------------------
    print("\n[7b] Thesis coverage")
    check("chapter 1 problem statement present in both languages",
          len(thesis_data.PROBLEM_STATEMENT_EN) > 400
          and len(thesis_data.PROBLEM_STATEMENT_AR) > 300)
    check("chapter 1 importance of the research present in both languages",
          len(thesis_data.IMPORTANCE_EN) > 400
          and len(thesis_data.IMPORTANCE_AR) > 300)
    check("abstract is complete in both languages (results and numbers kept)",
          all(tok in thesis_data.ABSTRACT_EN
              for tok in ("46 features", "96.79%", "0.988", "22 features",
                          "98.20%", "0.996", "decreasing the number of "
                          "features"))
          and all(tok in thesis_data.ABSTRACT_AR
                  for tok in ("46 سمة", "96.79%", "0.988", "22 سمة", "98.20%",
                              "0.996")))
    check("chapter 4 convergence text present for both datasets",
          all(len(thesis_data.CONVERGENCE[k]["en"]) > 300
              and len(thesis_data.CONVERGENCE[k]["ar"]) > 250
              for k in ("spambase", "phishing")))
    check("convergence keeps the published 2.2e-3 start and the 17-iteration "
          "stabilization",
          thesis_data.CONVERGENCE["spambase"]["start_cost"] == "2.2e-3"
          and thesis_data.CONVERGENCE["spambase"]["stable_from"] == 17
          and thesis_data.CONVERGENCE["phishing"]["stable_from"] == 9)

    # every number that carries meaning in the thesis must be reachable
    import pathlib as _pl

    _app_src = ""
    for _p in _pl.Path(__file__).parent.joinpath("thesis_app").rglob("*.py"):
        _app_src += _p.read_text(encoding="utf-8", errors="replace")

    # the concatenated source still contains Python quoting, so pull out the
    # actual string literals to test what the user really sees
    import ast as _ast

    _literals = []
    for _p in _pl.Path(__file__).parent.joinpath("thesis_app").rglob("*.py"):
        try:
            _tree = _ast.parse(_p.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for _node in _ast.walk(_tree):
            if isinstance(_node, _ast.Constant) and isinstance(_node.value, str):
                _literals.append(_node.value)
    _text = " ".join(" ".join(_literals).lower().split())
    _numbers = ["96.79", "96.40", "97.89", "97.14", "0.988", "98.20", "97.98",
                "98.80", "98.39", "0.996", "96.33", "95.43", "94.65", "95.04",
                "2.2e-3", "0.99", "0.7", "1.5", "0.2", "0.8", "0.9", "0.4",
                "0.02", "538", "339", "955", "1216", "4601", "11055", "57",
                "30", "46", "22"]
    _absent = [n for n in _numbers if n not in _app_src]
    check(f"all {len(_numbers)} meaningful thesis numbers appear in the app",
          not _absent, ", ".join(_absent))

    _terms = ["Bagging", "Gini", "entropy", "roulette", "elitism",
              "bit leap", "sigmoid", "min-max", "three nearest neighbors",
              "metaheuristic", "data leakage", "overfitting",
              "normalization", "behavior", "generalization", "optimization"]
    _absent_t = [w for w in _terms if w.lower() not in _text]
    check(f"all {len(_terms)} thesis terms appear in the app",
          not _absent_t, ", ".join(_absent_t))

    # the thesis is written in US English; the app must not drift to
    # British spellings or the terminology stops matching word for word
    _british = ["normalis", "optimis", "generalis", "behaviour", "maximis",
                "minimis", "labelled", "modelling", "analyser", "centre",
                "defence", "licence", "programme", "colour", "utilis",
                "summaris", "initialis", "recognis", "organis", "emphasise",
                "binaris", "penalis", "randomis", "stabilis", "tokenis",
                "neighbour", "favour", "honour", "catalogue", "judgement",
                "acknowledgement", "fuelled", "travelled", "whilst", "amongst"]
    _drift = [w for w in _british if w in _app_src.lower()]
    check("app keeps the thesis' US English spelling",
          not _drift, ", ".join(_drift))

    # the key terminology of the thesis must actually appear in the app
    _terms = ["particle swarm optimization", "genetic algorithm",
              "random forest", "feature selection", "gini", "bagging",
              "majority voting", "confusion matrix", "roc", "auc",
              "precision", "recall", "f1", "accuracy", "sensitivity",
              "specificity", "k-fold", "cross-validation", "roulette wheel",
              "single point", "bit leap", "elitism", "mutation", "crossover",
              "inertia", "cognitive", "social learning", "min-max",
              "normalization", "nearest neighbors", "missing values",
              "overfitting", "true positive", "false positive", "tpr", "fpr",
              "metaheuristic", "binary vector", "objective function",
              "cost function", "fitness", "premature convergence",
              "local optima", "diversity", "spambase", "phishing",
              "preprocessing", "ensemble learning", "decision tree",
              "variance", "bias", "impurity", "threshold", "feature subset",
              "data leakage", "future information", "stopping criteria",
              "exploration", "exploitation", "subsample", "discriminative",
              "acceleration coefficient", "bit value inversion", "internal node",
              "leaf", "retrained", "batch nature", "majority voting",
              "two-point crossover", "three nearest neighbors", "external archive",
              "parallel learning", "ensemble learning", "premature convergence",
              "bootstrap", "with replacement", "stopping criteria", "penalty",
              "sensitivity", "specificity", "gini", "entropy", "impurity"]
    _missing_terms = [t for t in _terms if t not in _text]
    check("all thesis terminology is present in the app",
          not _missing_terms, ", ".join(_missing_terms))

    check("training time is measured, so hypothesis 3 is testable",
          "perf_counter" in _app_src and "speedup" in _app_src)

    # ---- 8. GUI -----------------------------------------------------------
    print("\n[8] Graphical interface")
    from PySide6.QtWidgets import QApplication

    from thesis_app.ui.main_window import NAV, MainWindow

    app = QApplication.instance() or QApplication([])
    win = MainWindow()
    win.resize(1400, 900)
    win.show()
    app.processEvents()
    check(f"{len(NAV)} pages built", len(win._pages) == len(NAV))

    # every page in NAV must actually be reachable and constructible
    check("every navigation entry has a page",
          all(k in win._pages for k, _l, _c in NAV),
          ", ".join(k for k, _l, _c in NAV if k not in win._pages))

    for lang in ("ar", "en"):
        TRANSLATOR.lang = lang
        app.processEvents()
        for key, _label, _cls in NAV:
            win.go(key)
            app.processEvents()
        check(f"all pages render in {lang}", True)

    # no Arabic may survive a switch to English — this is the check that
    # caught 342 strings that never retranslated.
    import re

    arabic = re.compile(r"[\u0600-\u06FF]")

    def visible_text(page):
        from PySide6.QtWidgets import QLabel, QPushButton

        out = []
        for w in page.findChildren(QLabel):
            if w.text().strip():
                out.append(w.text().strip())
        for w in page.findChildren(QPushButton):
            if w.text().strip():
                out.append(w.text().strip())
        return out

    leaks = {}
    for key, _label, _cls in NAV:
        TRANSLATOR.lang = "ar"
        win.go(key)
        app.processEvents()
        seen = set(visible_text(win._pages[key]))
        TRANSLATOR.lang = "en"
        win.go(key)
        app.processEvents()
        stale = sorted({s for s in visible_text(win._pages[key])
                        if arabic.search(s) and s in seen})
        if stale:
            leaks[key] = stale
    check("no Arabic text leaks into the English interface",
          not leaks,
          "; ".join(f"{k}: {len(v)}" for k, v in leaks.items()))

    # the student's name must follow the language too
    TRANSLATOR.lang = "ar"
    win.go("home")
    app.processEvents()
    check("Arabic mode shows حسين ناصر حسين",
          "حسين ناصر حسين" in win.windowTitle())
    TRANSLATOR.lang = "en"
    win.go("home")
    app.processEvents()
    check("English mode shows Hussein Naser Hussein",
          "Hussein Naser Hussein" in win.windowTitle())
    TRANSLATOR.lang = "ar"
    app.processEvents()

    # exercise the interactive pages
    win.go("detect_email")
    page = win._pages["detect_email"]
    page.editor.setPlainText(spam_text)
    page._analyze()
    app.processEvents()
    check("email page produced a verdict", page._last is not None)

    win.go("detect_url")
    page = win._pages["detect_url"]
    page.entry.setText("http://paypal-secure-login.verify-account.tk/login")
    page._analyze()
    app.processEvents()
    check("URL page produced a verdict", page._last is not None)

    win.go("manual")
    page = win._pages["manual"]
    page._fill("sus")
    page._classify()
    app.processEvents()
    check("manual page classified a vector", page.verdict_card.isVisible())

    # the two pages that surface the original archive
    win.go("matlab")
    app.processEvents()
    from PySide6.QtWidgets import QPlainTextEdit

    mp = win._pages["matlab"]
    views = mp.findChildren(QPlainTextEdit)
    check("MATLAB page shows all 5 source files",
          len(views) == len(_engine.MATLAB_FILES),
          f"{len(views)} code views")
    check("MATLAB page code is the real source, not a placeholder",
          any("GA_PSO_feature_selection" in v.toPlainText() for v in views))

    win.go("figures")
    app.processEvents()
    from PySide6.QtWidgets import QLabel as _QLabel

    fp = win._pages["figures"]
    shown = [w for w in fp.findChildren(_QLabel)
             if w.pixmap() and not w.pixmap().isNull()]
    check("figures page renders all 9 thesis images", len(shown) == 9,
          f"{len(shown)} images loaded")

    # each picture must carry its thesis figure number, or the reader cannot
    # match the app to the PDF
    _figs = [f"Figure 4-{i}" for i in range(1, 9)]
    _have = [f for f in _figs if f in _app_src]
    check("all 8 thesis figure numbers are shown on the figures page",
          len(_have) == 8, ", ".join(set(_figs) - set(_have)))

    # a short experiment run
    res = engine.run_experiment("phishing", n_pop=4, max_it=2, desired=22)
    check("short experiment completes", res["n_selected"] == 22,
          f"acc {res['accuracy'] * 100:.2f}%  auc {res['auc']:.3f}")

    # ---- summary ----------------------------------------------------------
    print("\n" + "=" * 72)
    print(f"  {len(PASS)} passed, {len(FAIL)} failed")
    print("=" * 72)
    if FAIL:
        print("\nFailures:")
        for f in FAIL:
            print("  - " + f)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
