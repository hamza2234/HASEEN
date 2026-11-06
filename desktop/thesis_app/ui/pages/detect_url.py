"""Check-URL page: type any website address and the application derives the 30
Phishing-Websites attributes from the URL itself, then classifies it."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QHBoxLayout, QLineEdit, QVBoxLayout, QWidget)

from ...core import engine, feature_meta, url_analyzer
from ..i18n import signal_text, t
from ..widgets import (Card, ProbBars, VerdictBanner, make_table, muted,
                       paragraph)
from .base import BasePage

EX_FAKE = "http://paypal-secure-login.verify-account.tk/login.php?id=1"
EX_REAL = "https://www.paypal.com/signin"


class DetectURLPage(BasePage):
    def build(self):
        self._last = None

        # ---- input --------------------------------------------------------
        self.input_card = self.add_card("url.title", "url.intro")
        self.input_title = self.input_card.title_label
        self.input_hint = self.input_card.hint_label

        self.entry = QLineEdit()
        self.entry.setPlaceholderText(t("url.placeholder"))
        self.entry.setLayoutDirection(Qt.LeftToRight)
        self.entry.returnPressed.connect(self._analyze)
        self.input_card.add(self.entry)

        row = QWidget()
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(10)
        self.analyze_btn = self.button("common.analyze")
        self.analyze_btn.setObjectName("Primary")
        self.analyze_btn.setCursor(Qt.PointingHandCursor)
        self.analyze_btn.clicked.connect(self._analyze)
        self.fake_btn = self.button("url.example_fake")
        self.fake_btn.setObjectName("Ghost")
        self.fake_btn.clicked.connect(lambda: self.entry.setText(EX_FAKE))
        self.real_btn = self.button("url.example_real")
        self.real_btn.setObjectName("Ghost")
        self.real_btn.clicked.connect(lambda: self.entry.setText(EX_REAL))
        for b in (self.analyze_btn, self.fake_btn, self.real_btn):
            rl.addWidget(b)
        rl.addStretch(1)
        self.input_card.add(row)

        # ---- verdict -------------------------------------------------------
        self.verdict_card = Card()
        self.banner = VerdictBanner()
        self.verdict_card.add(self.banner)
        self.probs = ProbBars()
        self.verdict_card.add(self.probs)
        self.add(self.verdict_card)

        # ---- meta + signals -------------------------------------------------
        self.info_card = self.add_card("url.signals")
        self.info_title = self.info_card.title_label
        self.info_holder = QWidget()
        self.info_lay = QVBoxLayout(self.info_holder)
        self.info_lay.setContentsMargins(0, 0, 0, 0)
        self.info_card.add(self.info_holder)

        # ---- all 30 attributes ---------------------------------------------
        # the per-attribute table is the raw derivation; the verdict, the meta
        # facts and the risk signals answer the question on their own, so the
        # table is folded away.
        self.attr_sec = self.add_section("url.attributes")
        self.attr_holder = QWidget()
        self.attr_lay = QVBoxLayout(self.attr_holder)
        self.attr_lay.setContentsMargins(0, 0, 0, 0)
        self.attr_sec.add(self.attr_holder)

        self.verdict_card.setVisible(False)
        self.info_card.setVisible(False)
        self.attr_sec.setVisible(False)
        self.stretch()

    # ------------------------------------------------------------------ #
    def _analyze(self):
        url = self.entry.text().strip()
        if not url:
            self.banner.show_verdict(False, t("url.empty"), "")
            self.probs.set_probs([], [])
            self.verdict_card.setVisible(True)
            return
        if "." not in url:
            self.banner.show_verdict(False, t("url.invalid"), "")
            self.probs.set_probs([], [])
            self.verdict_card.setVisible(True)
            return

        values, res = url_analyzer.feature_vector(url)
        verdict = engine.predict_raw("phishing", values)
        self._last = (values, res, verdict)

        is_fake = verdict["is_fake"]
        title = t("url.verdict_fake") if is_fake else t("url.verdict_real")
        sub = (f"{t('common.confidence')}: {verdict['confidence'] * 100:.1f}%"
               f"   ·   {t('url.domain')}: {res['meta']['registrable'] or '—'}")
        self.banner.show_verdict(is_fake, title, sub)
        self.probs.set_probs(verdict["class_names"], verdict["probabilities"])
        self.verdict_card.setVisible(True)

        # meta facts
        self._clear(self.info_lay)
        m = res["meta"]
        self.info_lay.addWidget(make_table(
            [t("common.value"), t("common.meaning")],
            [[t("url.domain"), m["host"] or "—"],
             [t("url.registrable"), m["registrable"] or "—"],
             [t("url.tld"), m["tld"] or "—"],
             [t("url.https"), t("common.yes") if m["https"] else t("common.no")],
             [t("url.length"), m["length"]]],
            stretch_col=1, max_height=210))
        signals = res.get("signals") or []
        head = self.label("url.signals")
        head.setObjectName("CardTitle")
        self.info_lay.addWidget(head)
        if signals:
            self.info_lay.addWidget(paragraph(
                "•  " + "\n•  ".join(signal_text(s) for s in signals)))
        else:
            self.info_lay.addWidget(muted(t("url.no_signals")))
        self.info_card.setVisible(True)

        # all 30 attributes with their legend
        self._clear(self.attr_lay)
        lang = _lang()
        order = [n for n, _, _ in feature_meta.PHISHING_FEATURES]
        rows = []
        for name in order:
            val = res["features"][name]
            rows.append([feature_meta.label(name, lang), val,
                         feature_meta.meaning(name, val, lang)])
        self.attr_lay.addWidget(make_table(
            [t("common.feature"), t("common.value"), t("common.meaning")],
            rows, stretch_col=2, max_height=430))
        self.attr_sec.setVisible(True)

    @staticmethod
    def _clear(lay):
        while lay.count():
            item = lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()

    def retranslate(self):
        super().retranslate()
        self.entry.setPlaceholderText(t("url.placeholder"))
        if self._last is not None:
            values, res, verdict = self._last
            is_fake = verdict["is_fake"]
            title = (t("url.verdict_fake") if is_fake
                     else t("url.verdict_real"))
            sub = (f"{t('common.confidence')}: "
                   f"{verdict['confidence'] * 100:.1f}%")
            self.banner.show_verdict(is_fake, title, sub)
            self._analyze()


def _lang() -> str:
    from ..i18n import TRANSLATOR

    return TRANSLATOR.lang
