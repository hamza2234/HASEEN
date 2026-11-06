"""Datasets page: the two benchmark datasets, their classes and sizes, with the
raw attribute lists and a live preview of the real data folded into
collapsible sections.

The page used to open with 57 + 30 attribute names and two preview tables all
expanded, which buried the two facts a reader actually wants first: how big
each dataset is and how many attributes PSO-GA kept.
"""
from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QWidget

from ...core import engine, feature_meta
from ..i18n import pick
from ..widgets import KVBlock, StatTile, make_table, muted, paragraph
from .base import BasePage


DATASET_INFO = {
    "spambase": {
        "en": "UCI Spambase. Each row is one e-mail described by 57 numeric "
              "attributes: 48 word frequencies, 6 character frequencies and "
              "3 statistics about runs of capital letters. Class 1 = spam, "
              "class 0 = ham.",
        "ar": "مجموعة Spambase من UCI. كل صف بريد إلكتروني موصوف بـ 57 سمة "
              "عددية: 48 تكرار كلمة، و6 تكرار محارف، و3 إحصاءات عن سلاسل "
              "الأحرف الكبيرة. الفئة 1 = بريد مزعج، والفئة 0 = بريد سليم.",
    },
    "phishing": {
        "en": "UCI Phishing Websites. Each row is one website described by 30 "
              "attributes, each taking -1, 0 or 1. Class 1 = phishing, "
              "class -1 = legitimate. Note: this copy stores many attributes "
              "with the opposite sign to the official .arff file, so the "
              "application derives the meaning of each value from the data "
              "itself.",
        "ar": "مجموعة Phishing Websites من UCI. كل صف موقع موصوف بـ 30 سمة، "
              "كل واحدة تأخذ -1 أو 0 أو 1. الفئة 1 = تصيّد، والفئة -1 = موقع "
              "سليم. ملاحظة: هذه النسخة تخزّن سمات كثيرة بإشارة معاكسة لملف "
              ".arff الرسمي، لذلك يستنتج التطبيق معنى كل قيمة من البيانات "
              "نفسها.",
    },
}


class DatasetsPage(BasePage):
    #: every string here is computed from the data or through
    #: ``pick``, so the page is rebuilt when the language changes.
    rebuildable = True

    def build(self):
        for key in ("spambase", "phishing"):
            cfg = engine.THESIS[key]
            card = self.add_card(cfg["dataset"])
            card.add(paragraph(pick((DATASET_INFO[key]["en"],
                                     DATASET_INFO[key]["ar"]))))

            # the four headline numbers, in one row
            tiles = [
                StatTile(pick(("Samples", "عدد العينات")),
                         f"{cfg['n_samples']:,}"),
                StatTile(pick(("Attributes", "عدد السمات")),
                         str(cfg["n_features"])),
                StatTile(pick(("Selected by PSO-GA", "اخترتها PSO–GA")),
                         str(cfg["n_selected"])),
                StatTile(pick(("Classes", "الفئات")), "2"),
            ]
            row = QWidget()
            rl = QHBoxLayout(row)
            rl.setContentsMargins(0, 0, 0, 0)
            rl.setSpacing(12)
            for tile in tiles:
                rl.addWidget(tile)
            card.add(row)

            # class balance on one line
            dist = engine.load_raw(key)[1]
            counts = {int(v): int((dist == v).sum())
                      for v in set(dist.tolist())}
            card.add(muted("   ·   ".join(
                f"{pick(('class', 'الفئة'))} {k}: {v:,} "
                f"({v / dist.size * 100:.1f}%)"
                for k, v in sorted(counts.items()))))

            # ---- the raw detail, folded away -----------------------------
            names = feature_meta.FEATURE_NAMES[key]
            half = (len(names) + 1) // 2
            sec = self.add_section("data.columns")
            pairs = [(str(i + 1), n) for i, n in enumerate(names[:half])]
            pairs2 = [(str(i + half + 1), n)
                      for i, n in enumerate(names[half:])]
            cols = QWidget()
            cl = QHBoxLayout(cols)
            cl.setContentsMargins(0, 0, 0, 0)
            cl.setSpacing(18)
            cl.addWidget(KVBlock(lambda p=pairs: p), 1)
            cl.addWidget(KVBlock(lambda p=pairs2: p), 1)
            sec.add(cols)

            prev = self.add_section("data.sample_preview")
            X, y, _ = engine.load_raw(key)
            n_cols = min(6, X.shape[1])
            headers = [f"x{i + 1}" for i in range(n_cols)] + [
                pick(("label", "الفئة"))]
            rows = [[f"{v:.3f}" for v in X[r, :n_cols]] + [int(y[r])]
                    for r in range(5)]
            prev.add(make_table(headers, rows, max_height=210))

        self.stretch()
