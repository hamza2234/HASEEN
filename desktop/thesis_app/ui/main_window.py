"""Application shell: sidebar navigation, header, language switch.

Pages are created lazily and cached, so start-up stays fast and switching
between pages is instant.
"""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QButtonGroup, QComboBox, QFrame,
                               QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QStackedWidget, QVBoxLayout, QWidget)

from ..core import thesis_data
from . import theme
from .i18n import TRANSLATOR, t
from .pages.about import AboutPage
from .pages.algorithm import AlgorithmPage
from .pages.datasets import DatasetsPage
from .pages.detect_email import DetectEmailPage
from .pages.detect_url import DetectURLPage
from .pages.experiment import ExperimentPage
from .pages.figures import FiguresPage
from .pages.home import HomePage
from .pages.matlab import MatlabPage
from .pages.manual import ManualPage
from .pages.results import ResultsPage

#: (key, i18n key for the nav label, page class)
NAV = [
    ("home", "nav.home", HomePage),
    ("detect_email", "nav.detect_email", DetectEmailPage),
    ("detect_url", "nav.detect_url", DetectURLPage),
    ("manual", "nav.manual", ManualPage),
    ("experiment", "nav.experiment", ExperimentPage),
    ("results", "nav.results", ResultsPage),
    ("dataset", "nav.dataset", DatasetsPage),
    ("algorithm", "nav.algorithm", AlgorithmPage),
    ("figures", "nav.figures", FiguresPage),
    ("matlab", "nav.matlab", MatlabPage),
    ("about", "nav.about", AboutPage),
]

#: Navigation grouped under short headings, so the eleven entries read as four
#: intentions (try it / the thesis / the evidence / the rest) rather than one
#: long list. Every key must appear in ``NAV``.
NAV_GROUPS = [
    ("nav.grp.start", ["home"]),
    ("nav.grp.try", ["detect_email", "detect_url", "manual"]),
    ("nav.grp.experiment", ["experiment", "results"]),
    ("nav.grp.thesis", ["dataset", "algorithm", "figures", "matlab", "about"]),
]



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        theme.load_fonts()
        self.setObjectName("Root")
        self.setWindowTitle(self._window_title())
        self.resize(1280, 820)
        self.setMinimumSize(1060, 680)
        self.setStyleSheet(theme.stylesheet())

        self._pages: dict[str, QWidget] = {}
        self._nav_buttons: dict[str, QPushButton] = {}

        root = QWidget()
        root.setObjectName("Root")
        self.setCentralWidget(root)
        outer = QHBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        outer.addWidget(self._build_sidebar())

        right = QWidget()
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(0, 0, 0, 0)
        right_lay.setSpacing(0)
        right_lay.addWidget(self._build_header())
        self.stack = QStackedWidget()
        right_lay.addWidget(self.stack, 1)
        outer.addWidget(right, 1)

        self._build_pages()
        self._apply_direction()
        self.go("home")

        TRANSLATOR.changed.connect(self._on_language_changed)

    # ------------------------------------------------------------------ #
    #  Shell construction                                                 #
    # ------------------------------------------------------------------ #
    def _build_sidebar(self) -> QFrame:
        bar = QFrame()
        bar.setObjectName("Sidebar")
        bar.setFixedWidth(244)
        lay = QVBoxLayout(bar)
        lay.setContentsMargins(14, 18, 14, 16)
        lay.setSpacing(4)

        # brand: a small gradient badge plus the two text lines
        brand_row = QWidget()
        brl = QHBoxLayout(brand_row)
        brl.setContentsMargins(2, 0, 2, 0)
        brl.setSpacing(10)
        badge = QFrame()
        badge.setObjectName("BrandBadge")
        badge.setFixedSize(38, 38)
        bl = QVBoxLayout(badge)
        bl.setContentsMargins(0, 0, 0, 0)
        badge_text = QLabel("PSO")
        badge_text.setObjectName("BrandBadgeText")
        badge_text.setAlignment(Qt.AlignCenter)
        bl.addWidget(badge_text)
        brl.addWidget(badge)

        col = QVBoxLayout()
        col.setContentsMargins(0, 0, 0, 0)
        col.setSpacing(1)
        self.brand = QLabel(t("app.short"))
        self.brand.setObjectName("Brand")
        self.brand_sub = QLabel(t("app.subtitle"))
        self.brand_sub.setObjectName("BrandSub")
        self.brand_sub.setWordWrap(True)
        col.addWidget(self.brand)
        col.addWidget(self.brand_sub)
        brl.addLayout(col, 1)
        lay.addWidget(brand_row)
        lay.addSpacing(12)

        # navigation, grouped under short headings
        self.group = QButtonGroup(self)
        self.group.setExclusive(True)
        self._nav_groups: list[tuple[QLabel, list[QPushButton]]] = []
        by_key = {k: (label_key, cls) for k, label_key, cls in NAV}
        for group_key, keys in NAV_GROUPS:
            heading = QLabel(t(group_key))
            heading.setObjectName("NavGroup")
            heading.setProperty("_i18n_key", group_key)
            lay.addWidget(heading)
            buttons = []
            for key in keys:
                label_key, _cls = by_key[key]
                btn = QPushButton(t(label_key))
                btn.setObjectName("NavItem")
                btn.setCheckable(True)
                btn.setCursor(Qt.PointingHandCursor)
                btn.clicked.connect(lambda _=False, k=key: self.go(k))
                self.group.addButton(btn)
                self._nav_buttons[key] = btn
                buttons.append(btn)
                lay.addWidget(btn)
            self._nav_groups.append((heading, buttons))
            lay.addSpacing(10)

        lay.addStretch(1)

        self.lang_label = QLabel(t("common.language"))
        self.lang_label.setObjectName("Muted")
        self.lang_combo = QComboBox()
        self.lang_combo.addItem(t("common.arabic"), "ar")
        self.lang_combo.addItem(t("common.english"), "en")
        self.lang_combo.currentIndexChanged.connect(self._on_lang_combo)
        lay.addWidget(self.lang_label)
        lay.addWidget(self.lang_combo)
        return bar

    def _build_header(self) -> QFrame:
        head = QFrame()
        head.setObjectName("Header")
        head.setFixedHeight(78)
        lay = QHBoxLayout(head)
        lay.setContentsMargins(26, 12, 26, 12)
        lay.setSpacing(12)
        col = QVBoxLayout()
        col.setContentsMargins(0, 0, 0, 0)
        col.setSpacing(2)
        self.page_title = QLabel("")
        self.page_title.setObjectName("PageTitle")
        self.page_sub = QLabel("")
        self.page_sub.setObjectName("PageSub")
        self.page_sub.setWordWrap(True)
        col.addWidget(self.page_title)
        col.addWidget(self.page_sub)
        lay.addLayout(col, 1)
        self.header_note = QLabel(self._student_name())
        self.header_note.setObjectName("HeaderName")
        lay.addWidget(self.header_note, 0, Qt.AlignVCenter)
        return head

    def _build_pages(self):
        for key, _label, cls in NAV:
            page = cls()
            self._pages[key] = page
            self.stack.addWidget(page)

    # ------------------------------------------------------------------ #
    #  Navigation                                                         #
    # ------------------------------------------------------------------ #
    def go(self, key: str):
        page = self._pages.get(key)
        if page is None:
            return
        self.stack.setCurrentWidget(page)
        btn = self._nav_buttons.get(key)
        if btn is not None:
            btn.setChecked(True)
        self.page_title.setText(t(dict((k, l) for k, l, _ in NAV)[key]))
        self.page_sub.setText(self._page_subtitle(key))
        if hasattr(page, "on_show"):
            page.on_show()

    def _page_subtitle(self, key: str) -> str:
        mapping = {
            "home": t("app.tagline"),
            "dataset": t("data.intro"),
            "algorithm": t("algo.intro"),
            "experiment": t("exp.intro"),
            "results": t("res.intro"),
            "detect_email": t("mail.intro"),
            "detect_url": t("url.intro"),
            "manual": t("man.intro"),
            "matlab": t("matlab.intro"),
            "figures": t("fig.intro"),
            "about": t("about.title"),
        }
        return mapping.get(key, "")

    # ------------------------------------------------------------------ #
    #  Language                                                           #
    # ------------------------------------------------------------------ #
    def _on_lang_combo(self, _index: int):
        lang = self.lang_combo.currentData()
        if lang != TRANSLATOR.lang:
            TRANSLATOR.lang = lang

    @staticmethod
    def _student_name() -> str:
        c = thesis_data.COVER
        return c["student_ar"] if TRANSLATOR.is_rtl else c["student"]

    def _window_title(self) -> str:
        return f"{t('app.name')} — {self._student_name()}"

    def _on_language_changed(self, lang: str):
        self.setWindowTitle(self._window_title())
        self.header_note.setText(self._student_name())
        self.brand.setText(t("app.short"))
        self.brand_sub.setText(t("app.subtitle"))
        self.lang_label.setText(t("common.language"))
        for key, label_key, _cls in NAV:
            self._nav_buttons[key].setText(t(label_key))
        for heading, _buttons in self._nav_groups:
            heading.setText(t(heading.property("_i18n_key") or ""))
        current = self.stack.currentWidget()
        for key, page in self._pages.items():
            if page is current:
                self.page_title.setText(t(dict((k, l) for k, l, _ in NAV)[key]))
                self.page_sub.setText(self._page_subtitle(key))
        # keep the combo in sync when the language was changed elsewhere
        idx = self.lang_combo.findData(lang)
        if idx >= 0 and idx != self.lang_combo.currentIndex():
            self.lang_combo.blockSignals(True)
            self.lang_combo.setCurrentIndex(idx)
            self.lang_combo.blockSignals(False)
        for page in self._pages.values():
            if hasattr(page, "retranslate"):
                page.retranslate()
        self._apply_direction()

    def _apply_direction(self):
        if TRANSLATOR.is_rtl:
            self.setLayoutDirection(Qt.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LeftToRight)
        # Typography is direction-dependent (font face and letter-spacing both
        # change with the language), so both are rebuilt on every switch.
        app = QApplication.instance()
        if app is not None:
            app.setFont(theme.base_font(10))
        self.setStyleSheet(theme.stylesheet())
