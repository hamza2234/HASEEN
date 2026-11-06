"""Check-email page: paste any e-mail text, the application extracts the 57
Spambase attributes from it and classifies it spam (fake) or ham (real)."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QHBoxLayout, QTextEdit, QVBoxLayout, QWidget)

from ...core import engine, text_analyzer
from ..i18n import pick, sep, t
from ..widgets import (Card, ProbBars, VerdictBanner, make_table, muted,
                       paragraph)
from .base import BasePage

EX_SPAM = (
    "Subject: URGENT!!! Your account will be suspended\n\n"
    "Dear customer, we detected unusual activity on your account. You must "
    "verify your password and credit card details immediately or your account "
    "will be closed. Click here now to confirm your information. This is a "
    "limited time offer and free money $5000 prize is waiting for you. Act "
    "now! Call 1-800-555-0199. Reply with your bank account number today."
)

EX_HAM = (
    "Subject: Project meeting tomorrow at 10am\n\n"
    "Hi George, just a reminder that our project meeting is tomorrow at 10am "
    "in the conference room on the second floor. Please bring the report and "
    "the data table we discussed last week. Let me know if that time still "
    "works for you. Thanks, Maria. Dept of Computer Science."
)


class DetectEmailPage(BasePage):
    def build(self):
        self._last = None

        # ---- input --------------------------------------------------------
        self.input_card = self.add_card("mail.title", "mail.intro")
        self.input_title = self.input_card.title_label
        self.input_hint = self.input_card.hint_label

        self.editor = QTextEdit()
        self.editor.setPlaceholderText(t("mail.placeholder"))
        self.editor.setFixedHeight(190)
        self.input_card.add(self.editor)

        row = QWidget()
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(10)
        self.analyze_btn = self.button("common.analyze")
        self.analyze_btn.setObjectName("Primary")
        self.analyze_btn.setCursor(Qt.PointingHandCursor)
        self.analyze_btn.clicked.connect(self._analyze)
        self.spam_btn = self.button("mail.example_spam")
        self.spam_btn.setObjectName("Ghost")
        self.spam_btn.clicked.connect(lambda: self.editor.setPlainText(EX_SPAM))
        self.ham_btn = self.button("mail.example_ham")
        self.ham_btn.setObjectName("Ghost")
        self.ham_btn.clicked.connect(lambda: self.editor.setPlainText(EX_HAM))
        self.clear_btn = self.button("common.clear")
        self.clear_btn.setObjectName("Ghost")
        self.clear_btn.clicked.connect(self._clear)
        for b in (self.analyze_btn, self.spam_btn, self.ham_btn,
                  self.clear_btn):
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

        # ---- drivers -------------------------------------------------------
        self.driver_card = self.add_card("mail.top_features")
        self.driver_title = self.driver_card.title_label
        self.driver_holder = QWidget()
        self.driver_lay = QVBoxLayout(self.driver_holder)
        self.driver_lay.setContentsMargins(0, 0, 0, 0)
        self.driver_card.add(self.driver_holder)

        # ---- keywords ------------------------------------------------------
        self.kw_card = self.add_card("mail.keywords")
        self.kw_title = self.kw_card.title_label
        self.kw_holder = QWidget()
        self.kw_lay = QVBoxLayout(self.kw_holder)
        self.kw_lay.setContentsMargins(0, 0, 0, 0)
        self.kw_card.add(self.kw_holder)

        # ---- extracted features -------------------------------------------
        # the full 57-attribute vector is reference material: fold it away so
        # the verdict and the drivers stay the focus of the page.
        self.feat_sec = self.add_section("mail.features")
        self.feat_holder = QWidget()
        self.feat_lay = QVBoxLayout(self.feat_holder)
        self.feat_lay.setContentsMargins(0, 0, 0, 0)
        self.feat_sec.add(self.feat_holder)

        self.verdict_card.setVisible(False)
        self.driver_card.setVisible(False)
        self.kw_card.setVisible(False)
        self.feat_sec.setVisible(False)
        self.stretch()

    # ------------------------------------------------------------------ #
    def _clear(self):
        self.editor.clear()
        for card in (self.verdict_card, self.driver_card, self.kw_card,
                     self.feat_sec):
            card.setVisible(False)
        self._last = None

    def _analyze(self):
        text = self.editor.toPlainText().strip()
        if not text:
            self.banner.show_verdict(False, t("mail.empty"), "")
            self.probs.set_probs([], [])
            self.verdict_card.setVisible(True)
            return

        values = text_analyzer.extract_spambase_features(text)
        details = text_analyzer.explain_spambase(text)
        verdict = engine.predict_raw("spambase", values)
        self._last = (values, details, verdict)

        is_fake = verdict["is_fake"]
        title = t("mail.verdict_fake") if is_fake else t("mail.verdict_real")
        sub = (f"{t('common.confidence')}: {verdict['confidence'] * 100:.1f}%"
               f"   ·   {len(values)} {pick(('attributes', 'سمة'))}")
        if len(text.split()) < 8:
            sub += "   ·   " + t("mail.too_short")
        self.banner.show_verdict(is_fake, title, sub)
        self.probs.set_probs(verdict["class_names"], verdict["probabilities"])
        self.verdict_card.setVisible(True)

        # drivers
        self._clear_layout(self.driver_lay)
        rows = [[d["feature"], f"{d['value']:.3f}",
                 f"{d['importance'] * 100:.2f}%"] for d in verdict["drivers"]]
        self.driver_lay.addWidget(make_table(
            [t("common.feature"), t("common.value"),
             t("common.importance")], rows, max_height=230))
        self.driver_card.setVisible(True)

        # keywords
        self._clear_layout(self.kw_lay)
        hits = details.get("hits") or []
        if hits:
            chips = sep().join(
                f"{h['token']} ({h['percent']:.2f}%)" for h in hits)
            self.kw_lay.addWidget(paragraph(chips))
        else:
            self.kw_lay.addWidget(muted(
                pick(("No dataset keyword or symbol was found in the text.",
                      "لم تُوجد أي كلمة أو رمز من كلمات المجموعة في النص."))))
        self.kw_card.setVisible(True)

        # full feature vector
        self._clear_layout(self.feat_lay)
        from ...core import feature_meta

        names = feature_meta.FEATURE_NAMES["spambase"]
        shown = [(n, v) for n, v in zip(names, values) if v != 0]
        shown = shown[:40] if shown else list(zip(names, values))[:40]
        self.feat_lay.addWidget(muted(
            f"{len([v for v in values if v != 0])} / {len(values)} "
            + pick(("attributes are non-zero", "سمة غير صفرية"))))
        rows = [[n, f"{v:.3f}"] for n, v in shown]
        self.feat_lay.addWidget(make_table(
            [t("common.feature"), t("common.value")], rows,
            stretch_col=0, max_height=320))
        self.feat_sec.setVisible(True)

    @staticmethod
    def _clear_layout(lay):
        while lay.count():
            item = lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()

    def retranslate(self):
        super().retranslate()
        self.editor.setPlaceholderText(t("mail.placeholder"))
        # re-run the classification so every derived string (the attribute
        # count suffix, the driver table, the keyword list) follows the
        # language as well. Prediction is deterministic, so the verdict is
        # unchanged.
        if self._last is not None:
            self._analyze()
