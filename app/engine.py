"""GA-PSO + RandomForest feature-selection engine.

Self-contained re-implementation of the MATLAB sources shipped with the thesis
(main.m / GA_PSO_feature_selection.m / fitness_RF.m / repair_solution.m /
plot_results.m) so the web demo can run the experiment end-to-end and expose
every number, curve and matrix the thesis reports.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score,
                             roc_curve)
from sklearn.model_selection import train_test_split

from feature_meta import FEATURE_NAMES

EPS = np.finfo(float).eps

# --------------------------------------------------------------------------- #
#  Thesis published values (as printed in the PDF)                            #
# --------------------------------------------------------------------------- #
THESIS = {
    "spambase": {
        "title": "Spam Email Detection",
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
    },
    "phishing": {
        "title": "Phishing Website Detection",
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
    },
}

# Table 4-4 of the thesis
PARAMS_TABLE = [
    ("Max Iteration", "MaxIt", "20", "Number of times the optimisation process is executed"),
    ("Population Size", "nPop", "20", "Number of particles / chromosomes per iteration"),
    ("Inertia coefficient", "w", "0.7", "Balancing global and local search in PSO"),
    ("Cognitive learning coefficient", "c1", "1.5", "Effect of individual experience of each particle"),
    ("Social learning coefficient", "c2", "1.5", "Effect of best collective experience"),
    ("Crossover rate", "Pc", "0.8", "Probability of performing the combination operator"),
    ("Mutation rate", "Pm", "0.2", "Probability of random change of genes"),
    ("Parent selection", "-", "Roulette Wheel", "Select individuals based on fitness value"),
    ("Cross-validation", "K", "5", "K-Fold cross validation, prevent overfitting"),
    ("Crossover type", "-", "Single Point", "Generate new offspring from selected parents"),
    ("Mutation type", "-", "Bit Leap", "Randomly change the value of some genes"),
    ("Elitism", "-", "1 member", "Transfer the best solution unchanged"),
    ("Objective function", "-", "Combination Cost", "Minimise RF error and number of selected features"),
]

DATA_FILES = {
    "spambase": "extracted_zip/hussiandamghan/spambase.xlsx",
    "phishing": "extracted_zip/hussiandamghan/Data_phishing.xlsx",
}

# resolve data paths relative to the project root (parent of app/)
_ROOT = Path(__file__).resolve().parent.parent


# --------------------------------------------------------------------------- #
#  Data loading                                                               #
# --------------------------------------------------------------------------- #
def load_raw(key: str):
    """Return (X_raw, y, feature_names) without normalisation."""
    df = pd.read_excel(_ROOT / DATA_FILES[key], header=None)
    X = df.iloc[:, :-1].to_numpy(float)
    y = df.iloc[:, -1].to_numpy(int)
    names = FEATURE_NAMES.get(key) or [f"F{i+1}" for i in range(X.shape[1])]
    return X, y, names


def feature_ranges(key: str):
    """(min, max) per feature, taken over the whole dataset — the exact ranges
    main.m uses for min-max normalisation."""
    X, _, _ = load_raw(key)
    return X.min(0), X.max(0)


def normalise(X, lo, hi):
    return (X - lo) / (hi - lo + EPS)


def load_dataset(key: str):
    """Return (X_normalised, y, feature_names). Matches main.m: last column is
    the label, then min-max normalisation."""
    X, y, names = load_raw(key)
    lo, hi = X.min(0), X.max(0)
    return normalise(X, lo, hi), y, names


# --------------------------------------------------------------------------- #
#  Deployed model (trained on the whole dataset, used for live prediction)     #
# --------------------------------------------------------------------------- #
_MODEL_CACHE: dict = {}


def get_model(key: str, seed: int = 0):
    """Random-forest detector trained on the full dataset, with the
    normalisation ranges and feature names. Cached per (key, seed)."""
    ck = (key, seed)
    if ck not in _MODEL_CACHE:
        X, y, names = load_raw(key)
        lo, hi = X.min(0), X.max(0)
        rf = RandomForestClassifier(n_estimators=100, random_state=seed,
                                    n_jobs=-1)
        rf.fit(normalise(X, lo, hi), y)
        _MODEL_CACHE[ck] = {"rf": rf, "lo": lo, "hi": hi, "names": names}
    return _MODEL_CACHE[ck]


def predict_raw(key, raw_values, seed=0, top_k=6):
    """Classify one sample supplied in *raw* (un-normalised) feature units."""
    cfg = THESIS[key]
    m = get_model(key, seed)
    lo, hi, names = m["lo"], m["hi"], m["names"]
    v = np.asarray(raw_values, float)
    if v.size != lo.size:
        raise ValueError(f"expected {lo.size} features, got {v.size}")
    v = np.clip(v, lo, hi)
    vn = normalise(v, lo, hi).reshape(1, -1)

    proba = m["rf"].predict_proba(vn)[0]
    classes = m["rf"].classes_.tolist()
    pred = int(classes[int(np.argmax(proba))])

    if key == "spambase":
        label = "Spam / Fake" if pred == cfg["pos_label"] else "Ham / Real"
    else:
        label = ("Phishing / Fake" if pred == cfg["pos_label"]
                 else "Legitimate / Real")

    imp = m["rf"].feature_importances_
    order = np.argsort(imp)[::-1][:top_k]
    drivers = [{"feature": names[i], "importance": float(imp[i]),
                "value": float(v[i])} for i in order]

    return {
        "dataset_key": key,
        "prediction": pred,
        "prediction_label": label,
        "is_fake": pred == cfg["pos_label"],
        "confidence": float(proba.max()),
        "probabilities": proba.tolist(),
        "classes": classes,
        "class_names": cfg["class_names"],
        "drivers": drivers,
    }


# --------------------------------------------------------------------------- #
#  Core algorithm                                                             #
# --------------------------------------------------------------------------- #
def fitness(position, X, y, desired, n_estimators=50, seed=0):
    """fitness_RF.m — RandomForest accuracy on the selected features plus a
    penalty on the number of selected features."""
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
    """repair_solution.m — force the chromosome to hold exactly `desired` ones."""
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
    """GA_PSO_feature_selection.m — PSO velocity/position update, then GA
    crossover and mutation, with elite/global-best bookkeeping."""
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

        for i in range(n_pop):                      # mutation
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
    """plot_results.m — final RandomForest on the selected features and every
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

    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=test_size, random_state=seed, stratify=y)

    gbest, gbest_cost, curve = ga_pso(
        Xtr, ytr, n_pop, max_it, desired, seed=seed, progress=progress)
    selected = np.flatnonzero(gbest)

    res = evaluate(Xtr, ytr, Xte, yte, selected, cfg["pos_label"], seed=seed)
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
        "params": {"n_pop": n_pop, "max_it": max_it, "desired": desired,
                   "test_size": test_size, "seed": seed},
    })
    return res


def predict_sample(key, values=None, seed=0):
    """Classify a single sample as fake/real (spam/ham or phishing/legit).

    With ``values=None`` a random sample is drawn from a held-out test split so
    the reported confidence is realistic (not a training-set overfit)."""
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

    if key == "spambase":
        label = "Spam / Fake" if pred == cfg["pos_label"] else "Ham / Real"
    else:
        label = ("Phishing / Fake" if pred == cfg["pos_label"]
                 else "Legitimate / Real")

    return {
        "dataset_key": key,
        "prediction": pred,
        "prediction_label": label,
        "confidence": float(proba.max()),
        "probabilities": proba.tolist(),
        "classes": classes,
        "class_names": cfg["class_names"],
        "true_label": true_label,
        "correct": (None if true_label is None else pred == true_label),
    }


def sample_batch(key, n=8, seed=0):
    """Classify several held-out samples for a table of predictions."""
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
        if key == "spambase":
            lab = "Spam / Fake" if p == cfg["pos_label"] else "Ham / Real"
        else:
            lab = ("Phishing / Fake" if p == cfg["pos_label"]
                   else "Legitimate / Real")
        rows.append({
            "index": int(i),
            "true_label": int(yte[i]),
            "predicted": p,
            "label": lab,
            "confidence": float(proba[i].max()),
            "correct": bool(p == yte[i]),
        })
    return {"dataset_key": key, "rows": rows}
