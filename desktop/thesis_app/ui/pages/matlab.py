"""MATLAB source page: the original ``.m`` files that ship with the thesis,
shown verbatim, plus the artefacts the archive contains that only MATLAB can
open.

The five sources are ~2700 lines of code in total, so each file is folded into
its own collapsible section. The reader sees the run order and each file's
purpose first, then opens the listing they want.
"""
from __future__ import annotations

from PySide6.QtWidgets import QLabel

from ...core import engine
from ..i18n import t
from ..widgets import code_view, make_table, muted, paragraph
from .base import BasePage

#: (file name, i18n key for the purpose, i18n key for the card title)
SOURCES = [
    ("main.m", "matlab.p_main"),
    ("GA_PSO_feature_selection.m", "matlab.p_ga_pso"),
    ("fitness_RF.m", "matlab.p_fitness"),
    ("repair_solution.m", "matlab.p_repair"),
    ("plot_results.m", "matlab.p_plot"),
]


class MatlabPage(BasePage):
    #: the code text and the tables are computed, so rebuild the page on a
    #: language change rather than registering every widget.
    rebuildable = True

    def build(self):
        self.add(paragraph(t("matlab.intro")))

        # ---- the five sources, in execution order -------------------------
        rows, missing = [], []
        for name, purpose_key in SOURCES:
            try:
                text = engine.matlab_source(name)
            except FileNotFoundError:
                missing.append(name)
                continue
            rows.append([name, str(text.count("\n") + 1), t(purpose_key)])

        card = self.add_card("matlab.run_order", "matlab.run_order_hint")
        card.add(make_table(
            [t("matlab.file"), t("matlab.lines"), t("matlab.purpose")],
            rows, stretch_col=2, max_height=230))

        # ---- each source, folded away -------------------------------------
        for name, purpose_key in SOURCES:
            if name in missing:
                continue
            sec = self.add_section(purpose_key)
            sec.add(muted(t("matlab.verbatim")))
            sec.add(code_view(engine.matlab_source(name)))

        if missing:
            warn = QLabel(t("matlab.missing") + "  " + ", ".join(missing))
            warn.setObjectName("Muted")
            warn.setWordWrap(True)
            self.add(warn)
        else:
            self.add(muted(t("matlab.all_present")))

        # ---- the artefacts MATLAB alone can open --------------------------
        extra = []
        for name in engine.MATLAB_EXTRA_FILES:
            try:
                size = engine.asset_path("matlab", name).stat().st_size
            except FileNotFoundError:
                continue
            extra.append([name, f"{size / 1024:.1f} KB"])
        if extra:
            sec = self.add_section("matlab.extra")
            sec.add(muted(t("matlab.extra_hint")))
            sec.add(make_table(
                [t("matlab.file"), t("common.size")], extra, max_height=200))
            sec.add(muted(t("matlab.extra_note")))

        self.stretch()
