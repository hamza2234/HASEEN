"""Algorithm page: the stages of the hybrid method, every equation, the
Table 4-4 parameter list and the pre-processing steps.

Only the six stages are open by default. The equations, the parameter table and
the pre-processing list are long reference material, so they sit in collapsible
sections and the page opens at a readable length.
"""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ...core import engine, thesis_data
from .. import theme
from ..i18n import pick, t
from ..widgets import make_table, muted, paragraph
from .base import BasePage


class AlgorithmPage(BasePage):
    #: every string here is computed from the data or through
    #: ``pick``, so the page is rebuilt when the language changes.
    rebuildable = True

    def build(self):
        self.add(paragraph(t("algo.intro")))

        # ---- stage-by-stage, the part a reader needs first ----------------
        card = self.add_card("algo.stages")
        for i, stage in enumerate(thesis_data.ALGORITHM_STAGES, start=1):
            (en_name, en_sub, en_body, ar_name, ar_sub, ar_body) = stage
            box = QWidget()
            box.setObjectName("CardFlat")
            box.setStyleSheet(
                f"QWidget#CardFlat{{background:{theme.SURFACE_2};"
                f"border:1px solid {theme.BORDER}; border-radius:8px;}}")
            bl = QVBoxLayout(box)
            bl.setContentsMargins(16, 13, 16, 13)
            bl.setSpacing(5)
            title = QLabel(f"{i}.  " + pick((en_name, ar_name))
                           + "  —  " + pick((en_sub, ar_sub)))
            tf = title.font()
            tf.setBold(True)
            title.setFont(tf)
            title.setWordWrap(True)
            body = QLabel(pick((en_body, ar_body)))
            body.setWordWrap(True)
            body.setObjectName("Body")
            bl.addWidget(title)
            bl.addWidget(body)
            card.add(box)

        # ---- equations ----------------------------------------------------
        sec = self.add_section("algo.equations")
        for eq in thesis_data.EQUATIONS:
            box = QWidget()
            bl = QVBoxLayout(box)
            bl.setContentsMargins(0, 0, 0, 0)
            bl.setSpacing(6)
            head = QLabel(f"({eq['no']})  " + pick((eq["name_en"],
                                                     eq["name_ar"])))
            hf = head.font()
            hf.setBold(True)
            head.setFont(hf)
            head.setWordWrap(True)
            formula = QLabel(eq["plain"])
            formula.setAlignment(Qt.AlignCenter)
            formula.setStyleSheet(
                f"font-family:monospace; font-size:13px;"
                f"color:{theme.ACCENT_DARK}; background:{theme.SURFACE};"
                f"border:1px solid {theme.BORDER}; border-radius:7px;"
                f"padding:11px;")
            formula.setLayoutDirection(Qt.LeftToRight)
            note = QLabel(pick((eq["note_en"], eq["note_ar"])))
            note.setWordWrap(True)
            note.setObjectName("Muted")
            bl.addWidget(head)
            bl.addWidget(formula)
            bl.addWidget(note)
            sec.add(box)

        # ---- parameters (Table 4-4) ---------------------------------------
        sec = self.add_section("algo.params")
        rows = [[p[0], p[1], p[2], p[3]] for p in engine.PARAMS_TABLE]
        sec.add(make_table(
            [t("common.name"), t("common.symbol"), t("common.value"),
             t("common.description")],
            rows, stretch_col=3, max_height=430))
        sec.add(muted(pick((
            "Table 4-4 of the thesis. The application follows these values, "
            "because the body text contradicts some of them (see the Results "
            "page).",
            "الجدول 4-4 من الرسالة. يتبع التطبيق هذه القيم لأن نص الرسالة "
            "يخالف بعضها (انظر صفحة النتائج)."))))

        # ---- pre-processing ------------------------------------------------
        sec = self.add_section("algo.preprocessing")
        for item in thesis_data.PREPROCESSING:
            (en_title, en_sub, en_body, ar_title, ar_sub, ar_body) = item
            box = QWidget()
            bl = QVBoxLayout(box)
            bl.setContentsMargins(0, 0, 0, 0)
            bl.setSpacing(3)
            head = QLabel("•  " + pick((en_title, ar_title))
                          + " — " + pick((en_sub, ar_sub)))
            hf = head.font()
            hf.setBold(True)
            head.setFont(hf)
            head.setWordWrap(True)
            body = QLabel(pick((en_body, ar_body)))
            body.setWordWrap(True)
            body.setObjectName("Body")
            bl.addWidget(head)
            bl.addWidget(body)
            sec.add(box)

        self.stretch()
