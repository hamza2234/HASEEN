"""Thesis figures page: the nine result images exported from MATLAB in the
archive that accompanies the thesis, shown unchanged.

The gallery is the point, so the images stay open. The per-figure value table
was identical in structure for both datasets and only repeated the numbers the
Results page already shows, so it is folded into one collapsible section.
"""
from __future__ import annotations

from PySide6.QtWidgets import QLabel

from ...core import engine
from ..i18n import t
from ..widgets import ImageTile, image_grid, make_table, muted, paragraph
from .base import BasePage


class FiguresPage(BasePage):
    #: the captions and the value table are computed, so rebuild the page on a
    #: language change.
    rebuildable = True

    def build(self):
        self.add(paragraph(t("fig.intro")))

        missing = []
        for key, heading_key, hint_key in (
                ("spambase", "fig.spambase", "fig.spambase_hint"),
                ("phishing", "fig.phishing", "fig.phishing_hint")):
            card = self.add_card(heading_key, hint_key)
            tiles = []
            for filename, caption_key in engine.FIGURES[key]:
                try:
                    path = engine.asset_path("figures", filename)
                except FileNotFoundError:
                    missing.append(filename)
                    continue
                tiles.append(ImageTile(path, t(caption_key)))
            if tiles:
                card.add(image_grid(tiles, columns=2))
            card.add(muted(t("fig.open_hint")))

        # ---- the published numbers behind the pictures --------------------
        sec = self.add_section("fig.published_values")
        rows = []
        for key in ("spambase", "phishing"):
            cfg = engine.THESIS[key]
            rows.append([
                cfg["dataset"],
                f"{cfg['accuracy']:.2f}%",
                f"{cfg['auc']:.3f}",
                f"{cfg['n_selected']} / {cfg['n_features']}",
            ])
        sec.add(make_table(
            [t("common.dataset"), t("metric.accuracy"), t("metric.auc"),
             t("metric.features")], rows, max_height=160))
        sec.add(muted(t("fig.source_note")))

        if missing:
            warn = QLabel(t("fig.missing") + "  " + ", ".join(missing))
            warn.setObjectName("Muted")
            warn.setWordWrap(True)
            self.add(warn)

        self.stretch()
