"""Email text -> Spambase feature vector.

Implements the exact definitions UCI gives for the Spambase attributes:

* ``word_freq_WORD``  = 100 * (occurrences of WORD) / (total words)
* ``char_freq_CHAR``  = 100 * (occurrences of CHAR) / (total characters)
* ``capital_run_length_average`` = mean length of runs of capital letters
* ``capital_run_length_longest`` = longest run of capital letters
* ``capital_run_length_total``   = total number of capital letters

A word is "any string of alphanumeric characters bounded by non-alphanumeric
characters or end-of-string", exactly as the dataset documentation states.
"""
from __future__ import annotations

import re

from feature_meta import SPAMBASE_CHARS, SPAMBASE_WORDS

_WORD_RE = re.compile(r"[A-Za-z0-9]+")
_CAP_RUN_RE = re.compile(r"[A-Z]+")


def _tokenise(text: str):
    return [w.lower() for w in _WORD_RE.findall(text)]


def _capital_runs(text: str):
    return [len(m) for m in _CAP_RUN_RE.findall(text)]


def extract_spambase_features(text: str) -> list:
    """Return the 57 Spambase features for ``text`` (raw, un-normalised)."""
    words = _tokenise(text)
    n_words = max(len(words), 1)

    # character denominator follows the UCI definition: total characters
    n_chars = max(len(text), 1)

    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1

    feats = [100.0 * counts.get(w, 0) / n_words for w in SPAMBASE_WORDS]
    feats += [100.0 * text.count(c) / n_chars for c in SPAMBASE_CHARS]

    runs = _capital_runs(text)
    if runs:
        feats += [sum(runs) / len(runs), max(runs), sum(runs)]
    else:
        feats += [0.0, 0.0, 0.0]
    return feats


def explain_spambase(text: str, top: int = 12):
    """Human-readable breakdown of what the analyser found in ``text``."""
    words = _tokenise(text)
    n_words = max(len(words), 1)
    n_chars = max(len(text), 1)

    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1

    hits = []
    for w in SPAMBASE_WORDS:
        c = counts.get(w, 0)
        if c:
            hits.append({"token": w, "kind": "word", "count": c,
                         "percent": 100.0 * c / n_words})
    for c in SPAMBASE_CHARS:
        n = text.count(c)
        if n:
            hits.append({"token": c, "kind": "char", "count": n,
                         "percent": 100.0 * n / n_chars})
    hits.sort(key=lambda h: h["percent"], reverse=True)

    runs = _capital_runs(text)
    return {
        "n_words": len(words),
        "n_chars": len(text),
        "hits": hits[:top],
        "all_hits": hits,
        "cap_avg": (sum(runs) / len(runs)) if runs else 0.0,
        "cap_longest": max(runs) if runs else 0,
        "cap_total": sum(runs),
    }
