"""Home page: an introduction to the thesis, the student, the published
results and a short plain-language explanation of how the detector works.

The page is deliberately short. It opens with one gradient banner, then three
self-describing actions, then a compact results strip. The dense reference
material (cover fields, keywords, the full summary) lives on the About and
Results pages.
"""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QWidget

from ...core import engine, thesis_data
from ..i18n import pick, t
from ..widgets import (ActionCard, Card, HeroBanner, StatTile, lead, step_card)
from .base import BasePage



class HomePage(BasePage):
    #: every string here is computed from the data or through
    #: ``pick``, so the page is rebuilt when the language changes.
    rebuildable = True

    def build(self):
        self._hero()
        self._actions()
        self._glance()
        self._how()
        self.stretch()

    # ------------------------------------------------------------------ #
    #  Hero banner                                                        #
    # ------------------------------------------------------------------ #
    def _hero(self):
        hero = HeroBanner()
        c = thesis_data.COVER
        hero.kicker.setText(t("home.hero.kicker"))
        hero.title.setText(pick((c["title"], c["title_ar"])))
        hero.sub.setText(t("app.subtitle"))

        hero.name_caption.setText(t("home.hero.by"))
        hero.name.setText(pick((c["student"], c["student_ar"])))
        hero.affiliation.setText(t("home.hero.affiliation").format(
            sup=pick((c["supervisor"], c["supervisor_ar"]))))

        spam = engine.THESIS["spambase"]
        phish = engine.THESIS["phishing"]
        hero.set_chips([
            t("home.hero.chip_offline"),
            t("home.hero.chip_bilingual"),
            t("home.hero.chip_accuracy").format(
                spam=f"{spam['accuracy']:.2f}",
                phish=f"{phish['accuracy']:.2f}"),
        ])
        self.add(hero)

        # one short paragraph under the banner, not four
        intro = self.add(Card())
        intro.add(lead(t("home.intro")))

    # ------------------------------------------------------------------ #
    #  Action cards                                                       #
    # ------------------------------------------------------------------ #
    def _actions(self):
        holder = QWidget()
        grid = QGridLayout(holder)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(14)

        specs = (
            ("🔎", "home.act.detect", "detect_email", "home.act.open"),
            ("⌨️", "home.act.manual", "manual", "home.act.open"),
            ("⚙️", "home.act.experiment", "experiment", "home.act.run"),
        )
        for col, (icon, key, target, cta_key) in enumerate(specs):
            card = ActionCard(
                icon, t(f"{key}.title"), t(f"{key}.body"),
                on_click=lambda k=target: self._go(k))
            card.cta.setText(t(cta_key))
            grid.addWidget(card, 0, col)
            grid.setColumnStretch(col, 1)
        self.add(holder)

    # ------------------------------------------------------------------ #
    #  Results at a glance                                                #
    # ------------------------------------------------------------------ #
    def _glance(self):
        card = self.add_card("home.glance.title", "home.glance.hint")
        grid = QGridLayout()
        grid.setSpacing(12)
        grid.setHorizontalSpacing(12)

        # one row per dataset: its name, then the three headline numbers
        for row, key in enumerate(("spambase", "phishing")):
            cfg = engine.THESIS[key]
            name = QLabel(cfg["dataset"])
            name.setObjectName("CardTitle")
            name.setAlignment(Qt.AlignLeading | Qt.AlignVCenter)
            grid.addWidget(name, row, 0)
            for col, (label_key, field, fmt) in enumerate((
                    ("home.glance.accuracy", "accuracy", lambda v: f"{v}%"),
                    ("home.glance.selected", "n_selected",
                     lambda v: f"{v} / {cfg['n_features']}"),
                    ("home.glance.samples", "n_samples", lambda v: f"{v:,}"))):
                tile = StatTile(t(label_key), fmt(cfg[field]))
                grid.addWidget(tile, row, col + 1)
        grid.setColumnStretch(0, 0)
        for col in range(1, 4):
            grid.setColumnStretch(col, 1)
        card.add_layout(grid)

        row = QWidget()
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(10)
        btn = self.button("home.glance.details", "Ghost")
        btn.clicked.connect(lambda: self._go("results"))
        rl.addWidget(btn)
        rl.addStretch(1)
        card.add(row)

    # ------------------------------------------------------------------ #
    #  How it works                                                       #
    # ------------------------------------------------------------------ #
    def _how(self):
        card = self.add_card("home.how.title", "home.how.sub")
        grid = QGridLayout()
        grid.setSpacing(12)
        for i, (body_key, title_key) in enumerate((
                ("how.encode", "how.encode.title"),
                ("how.vote", "how.vote.title"),
                ("how.confidence", "how.confidence.title"),
                ("how.select", "how.select.title"))):
            box, _title, _body = step_card(
                i + 1, t(title_key), t(body_key))
            grid.addWidget(box, i // 2, i % 2)
        card.add_layout(grid)

    # ------------------------------------------------------------------ #
    def _go(self, key: str):
        win = self.window()
        if hasattr(win, "go"):
            win.go(key)
