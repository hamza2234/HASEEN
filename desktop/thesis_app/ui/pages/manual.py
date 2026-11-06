"""Manual page: set every attribute by hand and classify the resulting vector,
or inspect held-out samples from the dataset.

The 30 / 57 attribute editors are the point of the page, so they stay visible,
but they are grouped into short labeled bands and the batch-sample tooling is
folded into a collapsible section. The verdict appears directly above the
editors, where the eye already is after pressing the button.
"""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QComboBox, QGridLayout, QHBoxLayout, QLabel,
                               QScrollArea, QVBoxLayout, QWidget)

from ...core import engine, feature_meta
from .. import theme
from ..i18n import TRANSLATOR, t
from ..widgets import (Card, ProbBars, VerdictBanner, make_table, muted,
                       paragraph)
from .base import BasePage


#: Phishing attributes grouped by what they describe, so 30 editors read as
#: five short bands instead of one undifferentiated block. Order inside each
#: group follows the dataset column order, which is the order the vector needs.
PHISHING_GROUPS = [
    ("man.grp.url", [
        "having_IP_Address", "URL_Length", "Shortining_Service",
        "having_At_Symbol", "double_slash_redirecting", "Prefix_Suffix",
        "having_Sub_Domain",
    ]),
    ("man.grp.security", [
        "SSLfinal_State", "Domain_registeration_length", "Favicon", "port",
        "HTTPS_token",
    ]),
    ("man.grp.html", [
        "Request_URL", "URL_of_Anchor", "Links_in_tags", "SFH",
        "Submitting_to_email", "Abnormal_URL", "Redirect", "on_mouseover",
        "RightClick", "popUpWidnow", "Iframe",
    ]),
    ("man.grp.domain", [
        "age_of_domain", "DNSRecord", "web_traffic", "Page_Rank",
        "Google_Index", "Links_pointing_to_page", "Statistical_report",
    ]),
]

#: Spambase attributes grouped by kind, mirroring the UCI description.
SPAMBASE_GROUPS = [
    ("man.grp.word", feature_meta.SPAMBASE_WORDS),
    ("man.grp.char", feature_meta.SPAMBASE_CHARS),
    ("man.grp.caps", ["capital_run_length_average", "capital_run_length_longest",
                      "capital_run_length_total"]),
]


class ManualPage(BasePage):
    def build(self):
        self._dataset = "phishing"
        self._selects: dict[str, QComboBox] = {}

        self._controls()
        self._verdict()
        self._editors()
        self._batch()
        self._rebuild_editors()
        self.stretch()

    # ------------------------------------------------------------------ #
    #  Controls                                                           #
    # ------------------------------------------------------------------ #
    def _controls(self):
        card = self.add_card("man.title", "man.intro")
        card.add(self.keep(paragraph(t("man.howto")), "man.howto"))

        row = QWidget()
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(10)
        rl.addWidget(self.label("common.dataset"))
        self.dataset_combo = QComboBox()
        for key in ("phishing", "spambase"):
            self.dataset_combo.addItem(engine.THESIS[key]["dataset"], key)
        self.dataset_combo.currentIndexChanged.connect(self._switch_dataset)
        rl.addWidget(self.dataset_combo)
        rl.addStretch(1)

        self.classify_btn = self.button("man.classify", "Primary")
        self.classify_btn.clicked.connect(self._classify)
        rl.addWidget(self.classify_btn)
        card.add(row)

        # quick fill helpers on their own line, so the primary action stands out
        row2 = QWidget()
        rl2 = QHBoxLayout(row2)
        rl2.setContentsMargins(0, 0, 0, 0)
        rl2.setSpacing(8)
        rl2.addWidget(self.label("man.quickfill", "Muted"))
        for key, mode in (("man.all_suspicious", "sus"),
                          ("man.all_safe", "safe"),
                          ("man.load_sample", "sample"),
                          ("man.reset", "reset")):
            btn = self.button(key, "Ghost")
            if mode == "sample":
                btn.clicked.connect(self._load_sample)
            else:
                btn.clicked.connect(lambda _=False, m=mode: self._fill(
                    None if m == "reset" else m))
            rl2.addWidget(btn)
        rl2.addStretch(1)
        card.add(row2)

    # ------------------------------------------------------------------ #
    #  Verdict                                                            #
    # ------------------------------------------------------------------ #
    def _verdict(self):
        self.verdict_card = Card()
        self.banner = VerdictBanner()
        self.verdict_card.add(self.banner)
        self.probs = ProbBars()
        self.verdict_card.add(self.probs)
        self.verdict_card.setVisible(False)
        self.add(self.verdict_card)

    # ------------------------------------------------------------------ #
    #  Attribute editors                                                  #
    # ------------------------------------------------------------------ #
    def _editors(self):
        self.edit_card = self.add_card("man.attributes", "man.attributes_hint")
        self.edit_area = QScrollArea()
        self.edit_area.setWidgetResizable(True)
        self.edit_area.setMinimumHeight(300)
        self.edit_area.setMaximumHeight(430)
        self.edit_area.setStyleSheet(
            f"QScrollArea{{border:1px solid {theme.BORDER}; border-radius:8px;"
            f"background:{theme.SURFACE};}}")
        self.edit_holder = QWidget()
        self.edit_outer = QVBoxLayout(self.edit_holder)
        self.edit_outer.setContentsMargins(16, 14, 16, 14)
        self.edit_outer.setSpacing(16)
        self.edit_area.setWidget(self.edit_holder)
        self.edit_card.add(self.edit_area)

    def _batch(self):
        sec = self.add_section("man.sample_table")
        sec.add(self.keep(muted(t("man.sample_note")), "man.sample_note"))
        brow = QWidget()
        brl = QHBoxLayout(brow)
        brl.setContentsMargins(0, 0, 0, 0)
        brl.setSpacing(10)
        for key, n in (("man.random_sample", 1), ("man.batch", 10)):
            btn = self.button(key, "Ghost")
            btn.clicked.connect(lambda _=False, k=n: self._batch_run(k))
            brl.addWidget(btn)
        brl.addStretch(1)
        sec.add(brow)
        self.batch_holder = QWidget()
        self.batch_lay = QVBoxLayout(self.batch_holder)
        self.batch_lay.setContentsMargins(0, 0, 0, 0)
        sec.add(self.batch_holder)

    # ------------------------------------------------------------------ #
    def _rebuild_editors(self):
        while self.edit_outer.count():
            item = self.edit_outer.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()
        self._selects.clear()

        if self._dataset == "phishing":
            groups = PHISHING_GROUPS
            names = [n for n, _, _ in feature_meta.PHISHING_FEATURES]
        else:
            groups = [
                ("man.grp.word",
                 [f"word_freq_{w}" for w in feature_meta.SPAMBASE_WORDS]),
                ("man.grp.char",
                 [f"char_freq_{c}" for c in feature_meta.SPAMBASE_CHARS]),
                ("man.grp.caps", SPAMBASE_GROUPS[2][1]),
            ]
            names = feature_meta.FEATURE_NAMES["spambase"]

        for group_key, members in groups:
            present = [n for n in members if n in names]
            if not present:
                continue

            head = QLabel(t(group_key))
            head.setObjectName("CardTitle")
            self.edit_outer.addWidget(head)

            holder = QWidget()
            grid = QGridLayout(holder)
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setSpacing(10)
            for i, name in enumerate(present):
                grid.addWidget(self._editor(name), i // 3, i % 3)
            self.edit_outer.addWidget(holder)

    def _editor(self, name: str) -> QWidget:
        box = QWidget()
        bl = QVBoxLayout(box)
        bl.setContentsMargins(0, 0, 0, 0)
        bl.setSpacing(4)

        lang = _lang()
        if self._dataset == "phishing":
            text = feature_meta.label(name, lang)
        else:
            text = name
        lab = QLabel(text)
        lab.setObjectName("Muted")
        lab.setWordWrap(True)
        bl.addWidget(lab)

        combo = QComboBox()
        if self._dataset == "phishing":
            coding = feature_meta.PHISHING_CODING[name]
            for val in sorted(coding.values(), reverse=True):
                combo.addItem(f"{val} — "
                              f"{feature_meta.meaning(name, val, lang)}", val)
        else:
            for val in (0, 1, 2, 5, 10):
                combo.addItem(str(val), float(val))
            combo.setEditable(True)
            combo.setCurrentText("0")
        combo.setLayoutDirection(Qt.LeftToRight)
        self._selects[name] = combo
        bl.addWidget(combo)
        return box

    # ------------------------------------------------------------------ #
    def retranslate(self):
        super().retranslate()
        # attribute names and value meanings come from feature_meta, not the
        # string table, so the editor grid is rebuilt instead.
        self._rebuild_editors()
        if self.verdict_card.isVisible():
            self._classify()

    def _switch_dataset(self):
        self._dataset = self.dataset_combo.currentData()
        self._rebuild_editors()
        self.verdict_card.setVisible(False)

    # ------------------------------------------------------------------ #
    def _values(self):
        if self._dataset == "phishing":
            order = [n for n, _, _ in feature_meta.PHISHING_FEATURES]
            return [int(self._selects[n].currentData()) for n in order]
        order = feature_meta.FEATURE_NAMES["spambase"]
        out = []
        for n in order:
            try:
                out.append(float(self._selects[n].currentText()))
            except ValueError:
                out.append(0.0)
        return out

    def _fill(self, mode):
        if self._dataset != "phishing":
            if mode is None:
                for combo in self._selects.values():
                    combo.setCurrentText("0")
            return
        for name, combo in self._selects.items():
            coding = feature_meta.PHISHING_CODING[name]
            if mode == "sus":
                target = coding["sus"]
            elif mode == "safe":
                target = coding["safe"]
            else:
                target = feature_meta.PHISHING_NEUTRAL.get(
                    name, coding.get("mid", coding["safe"]))
            idx = combo.findData(target)
            if idx >= 0:
                combo.setCurrentIndex(idx)

    def _load_sample(self):
        import numpy as np

        X, _y, _ = engine.load_raw(self._dataset)
        rng = np.random.default_rng()
        idx = int(rng.integers(X.shape[0]))
        row = X[idx]
        names = (feature_meta.FEATURE_NAMES["spambase"]
                 if self._dataset == "spambase"
                 else [n for n, _, _ in feature_meta.PHISHING_FEATURES])
        for n, v in zip(names, row):
            combo = self._selects[n]
            if self._dataset == "phishing":
                j = combo.findData(int(v))
                if j >= 0:
                    combo.setCurrentIndex(j)
            else:
                combo.setCurrentText(f"{v:.3f}")

    # ------------------------------------------------------------------ #
    def _classify(self):
        values = self._values()
        verdict = engine.predict_raw(self._dataset, values)
        is_fake = verdict["is_fake"]
        if self._dataset == "phishing":
            title = (t("url.verdict_fake") if is_fake
                     else t("url.verdict_real"))
        else:
            title = (t("mail.verdict_fake") if is_fake
                     else t("mail.verdict_real"))
        sub = f"{t('common.confidence')}: {verdict['confidence'] * 100:.1f}%"
        self.banner.show_verdict(is_fake, title, sub)
        self.probs.set_probs(verdict["class_names"], verdict["probabilities"])
        self.verdict_card.setVisible(True)

    def _batch_run(self, n: int):
        while self.batch_lay.count():
            item = self.batch_lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()
        res = engine.sample_batch(self._dataset, n=n)
        rows = []
        for r in res["rows"]:
            rows.append([
                r["index"],
                r["true_label"],
                r["label"],
                f"{r['confidence'] * 100:.1f}%",
                "✔" if r["correct"] else "✘",
            ])
        self.batch_lay.addWidget(make_table(
            ["#", t("man.actual"), t("man.predicted"),
             t("common.confidence"), t("common.correct")],
            rows, max_height=380))


def _lang() -> str:
    return TRANSLATOR.lang
