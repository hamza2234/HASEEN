"""Results page: published thesis values next to values computed by this
application, plus every contradiction found inside the thesis.

The published numbers and the confusion matrix are open, because that is what
the page is for. The page-24 comparison, the contradictions table and the
convergence analysis are reference material and sit in collapsible sections.
"""
from __future__ import annotations

from PySide6.QtWidgets import QGridLayout, QLabel, QWidget

from ...core import engine, thesis_data
from ..i18n import pick, t
from ..widgets import KVBlock, StatTile, make_table, muted, paragraph
from .base import BasePage

METRIC_KEYS = [("accuracy", "Accuracy", "الدقة"),
               ("precision", "Precision", "الإحكام"),
               ("recall", "Recall", "الاستدعاء"),
               ("f1", "F1-score", "معيار F1")]


class ResultsPage(BasePage):
    #: every string here is computed from the data or through
    #: ``pick``, so the page is rebuilt when the language changes.
    rebuildable = True

    def build(self):
        self.add(paragraph(t("res.intro")))

        for key in ("spambase", "phishing"):
            cfg = engine.THESIS[key]
            card = self.add_card(cfg["dataset"])

            tiles = [
                StatTile(pick(("Accuracy", "الدقة")), f"{cfg['accuracy']}%"),
                StatTile(pick(("Precision", "الإحكام")), f"{cfg['precision']}%"),
                StatTile(pick(("Recall", "الاستدعاء")), f"{cfg['recall']}%"),
                StatTile(pick(("F1-score", "معيار F1")), f"{cfg['f1']}%"),
                StatTile(pick(("AUC", "المساحة تحت المنحنى")), f"{cfg['auc']}"),
                StatTile(pick(("Selected features", "السمات المختارة")),
                         f"{cfg['n_selected']} / {cfg['n_features']}"),
            ]
            row = QWidget()
            g = QGridLayout(row)
            g.setContentsMargins(0, 0, 0, 0)
            g.setSpacing(12)
            for i, tile in enumerate(tiles):
                g.addWidget(tile, i // 3, i % 3)
            card.add(row)

            # confusion matrix
            cm = cfg["confusion_matrix"]
            head = QLabel(pick(("Published confusion matrix",
                                "مصفوفة الالتباس المنشورة")))
            head.setObjectName("CardTitle")
            card.add(head)
            names = cfg["class_names"]
            card.add(make_table(
                ["", names[0], names[1]],
                [[names[0], cm[0][0], cm[0][1]],
                 [names[1], cm[1][0], cm[1][1]]],
                max_height=140))

            # page-24 numbers, when they differ
            p24 = thesis_data.CH4_PAGE24.get(key)
            if p24:
                sec = self.add_section("res.page24")
                sec.add(muted(t("res.page24_note")))
                rows = [[pick((en, ar)), f"{cfg[mk]}%", f"{p24[mk]}%"]
                        for mk, en, ar in METRIC_KEYS]
                sec.add(make_table(
                    [t("common.metric"), t("res.published"),
                     t("res.page24")], rows, max_height=200))

        # ---- contradictions ----------------------------------------------
        sec = self.add_section("res.conflicts")
        sec.add(muted(t("res.conflicts_intro")))
        rows = [[
            pick((c["topic_en"], c["topic_ar"])),
            pick((c["text_en"], c["text_ar"])),
            pick((c["table_en"], c["table_ar"])),
            pick((c["code_en"], c["code_ar"])),
        ] for c in thesis_data.CONFLICTS]
        sec.add(make_table(
            [t("res.topic"), t("res.text_says"), t("res.table_says"),
             t("res.code_says")], rows, stretch_col=1, max_height=430))

        # ---- convergence analysis -------------------------------------------
        sec = self.add_section("res.convergence")
        for key in ("spambase", "phishing"):
            cfg = engine.THESIS[key]
            cv = thesis_data.CONVERGENCE[key]
            fig = "Figure 4-1" if key == "spambase" else "Figure 4-5"
            fig_ar = "الشكل 4-1" if key == "spambase" else "الشكل 4-5"
            head = QLabel(f"{cfg['dataset']} — {pick((fig, fig_ar))}")
            hf = head.font()
            hf.setBold(True)
            head.setFont(hf)
            head.setWordWrap(True)
            sec.add(head)
            sec.add(KVBlock(lambda cv=cv: [
                (t("res.start_cost"), cv["start_cost"]),
                (t("res.final_cost"), cv["final_cost"]),
                (t("res.stable_from"), str(cv["stable_from"])),
            ]))
            sec.add(paragraph(pick((cv["en"], cv["ar"]))))

        # ---- conclusion ----------------------------------------------------
        card = self.add_card("res.conclusion")
        card.add(paragraph(pick((thesis_data.CONCLUSION_EN,
                                 thesis_data.CONCLUSION_AR))))

        self.stretch()
