"""About page: the thesis cover page, abstract, objectives, questions,
hypotheses, classifier facts, metrics, scope limits and the technology used.

Only the cover and the abstract are open. Everything else is reference material
that a reader consults on demand, so it sits in collapsible sections; the page
used to open at nearly 4000 pixels of continuously expanded text.
"""
from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ...core import thesis_data
from ..i18n import pick, sep, t
from ..widgets import KVBlock, make_table, muted, paragraph
from .base import BasePage


class AboutPage(BasePage):
    #: every string here is computed from the data or through
    #: ``pick``, so the page is rebuilt when the language changes.
    rebuildable = True

    def build(self):
        # ---- cover --------------------------------------------------------
        self.add_card("about.cover").add(KVBlock(self._cover_pairs))

        # ---- abstract -----------------------------------------------------
        self.add_card("about.abstract").add(paragraph(
            pick((thesis_data.ABSTRACT_EN, thesis_data.ABSTRACT_AR))))

        # ---- narrative sections -------------------------------------------
        for title_key, en, ar in (
                ("about.problem", thesis_data.PROBLEM_STATEMENT_EN,
                 thesis_data.PROBLEM_STATEMENT_AR),
                ("about.importance", thesis_data.IMPORTANCE_EN,
                 thesis_data.IMPORTANCE_AR)):
            sec = self.add_section(title_key)
            sec.add(paragraph(pick((en, ar))))

        # ---- objectives ----------------------------------------------------
        sec = self.add_section("about.objectives")
        for obj in thesis_data.OBJECTIVES:
            en_title, ar_title, en_body, ar_body = obj
            sec.add(self._bullet(pick((en_title, ar_title)),
                                 pick((en_body, ar_body))))

        # ---- questions & hypotheses ----------------------------------------
        sec = self.add_section("about.questions")
        for i, q in enumerate(thesis_data.QUESTIONS, start=1):
            sec.add(paragraph(f"{i}.  " + pick(q)))

        sec = self.add_section("about.hypotheses")
        for i, h in enumerate(thesis_data.HYPOTHESES, start=1):
            sec.add(paragraph(f"{i}.  " + pick(h)))

        # ---- classifier + metrics ------------------------------------------
        sec = self.add_section("about.classifier")
        rows = [[pick((en_k, ar_k)), pick((en_v, ar_v))]
                for en_k, en_v, ar_k, ar_v in thesis_data.CLASSIFIER_FACTS]
        sec.add(make_table(
            [t("common.name"), t("common.description")], rows,
            stretch_col=1, max_height=330))

        sec = self.add_section("about.metrics")
        rows = [[pick((en_name, ar_name)), formula,
                 pick((en_desc, ar_desc))]
                for en_name, ar_name, formula, en_desc, ar_desc
                in thesis_data.METRICS]
        sec.add(make_table(
            [t("common.metric"), pick(("Formula", "المعادلة")),
             t("common.description")], rows, stretch_col=2, max_height=330))

        # ---- scope ----------------------------------------------------------
        sec = self.add_section("about.scope")
        for item in thesis_data.SCOPE_LIMITS:
            en_t, en_b, ar_t, ar_b = item
            sec.add(self._bullet(pick((en_t, ar_t)), pick((en_b, ar_b))))

        # ---- technology -----------------------------------------------------
        sec = self.add_section("about.tech")
        sec.add(paragraph(t("about.tech_note")))
        sec.add(muted(t("about.license")))

        self.stretch()

    # ------------------------------------------------------------------ #
    @staticmethod
    def _bullet(title: str, body: str) -> QWidget:
        box = QWidget()
        bl = QVBoxLayout(box)
        bl.setContentsMargins(0, 0, 0, 0)
        bl.setSpacing(3)
        head = QLabel("•  " + title)
        hf = head.font()
        hf.setBold(True)
        head.setFont(hf)
        head.setWordWrap(True)
        text = QLabel(body)
        text.setWordWrap(True)
        text.setObjectName("Body")
        bl.addWidget(head)
        bl.addWidget(text)
        return box

    def _cover_pairs(self):
        c = thesis_data.COVER
        return [
            (pick(("University", "الجامعة")),
             pick((c["university"], c["university_ar"]))),
            (pick(("Degree", "الدرجة")),
             pick((c["degree"], c["degree_ar"]))),
            (pick(("Field of study", "التخصص")),
             pick((c["field"], c["field_ar"]))),
            (pick(("Title", "العنوان")),
             pick((c["title"], c["title_ar"]))),
            (pick(("Student", "الطالب")),
             pick((c["student"], c["student_ar"]))),
            (pick(("Supervisor", "المشرف")),
             pick((c["supervisor"], c["supervisor_ar"]))),
            (pick(("Date", "التاريخ")), pick((c["date"], c["date_ar"]))),
            (pick(("Keywords", "الكلمات المفتاحية")),
             sep().join(pick((c["keywords"], c["keywords_ar"])))),
        ]
