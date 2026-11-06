"""Visual theme: color palette, fonts and the global stylesheet.

The look is calm, modern and restrained - a single accent color, generous
spacing, soft hairline borders, no heavy shadows - so it reads as a normal
desktop utility rather than an "AI-generated" page.

Every color name here is part of the public surface: the pages and widgets
import them directly when they need to paint something Qt's stylesheet cannot
express (a chart line, a progress fill).
"""
from __future__ import annotations

from PySide6.QtGui import QFont, QFontDatabase

# --------------------------------------------------------------------------- #
#  Palette                                                                     #
# --------------------------------------------------------------------------- #
BG = "#f4f6fa"          # window background
SURFACE = "#ffffff"     # cards and panels
SURFACE_2 = "#f4f6fa"   # subtle fills
SURFACE_3 = "#eaeef6"   # pressed / deeper fills
BORDER = "#e4e8f0"      # hairlines
BORDER_STRONG = "#d3dae6"
TEXT = "#131c2b"        # primary text
TEXT_MUTED = "#64748b"  # secondary text
TEXT_FAINT = "#94a3b8"  # tertiary text
ACCENT = "#2563eb"      # single accent color
ACCENT_DARK = "#1d4ed8"
ACCENT_SOFT = "#eef3ff"
ACCENT_RING = "#bfd3ff"
GOOD = "#0f9d63"
GOOD_SOFT = "#e7f7ef"
BAD = "#dc4c4c"
BAD_SOFT = "#fdeceb"
WARN = "#b7791f"
WARN_SOFT = "#fdf5e6"

#: Hero banner gradient (deep indigo -> accent blue)
HERO_A = "#1e3a8a"
HERO_B = "#2563eb"
HERO_C = "#3b82f6"

RADIUS = "10px"
RADIUS_LG = "14px"
RADIUS_SM = "8px"

#: Preferred UI font stack. Segoe UI and Tahoma are present on the Windows
#: delivery target; Noto Sans Arabic and DejaVu Sans are bundled with the
#: application so the Arabic interface renders identically on a bare Linux or
#: Windows machine with no fonts of its own. Qt resolves Arabic per character,
#: so one stack covers both languages.
_FONT_STACK = ('"Segoe UI", "Noto Sans", "DejaVu Sans", Tahoma, Arial, '
               'sans-serif')
#: Arabic stack: Noto Sans Arabic first, then the Windows and generic faces.
_FONT_STACK_AR = ('"Noto Sans Arabic", "Segoe UI", "DejaVu Sans", Tahoma, '
                  'Arial, sans-serif')
#: Latin-first order, for the English interface.
_FONT_PREFERENCE = ("Segoe UI", "Noto Sans", "DejaVu Sans", "Tahoma", "Arial")
#: Arabic-first order, for the Arabic interface. Segoe UI covers Arabic on
#: Windows but its Arabic is a fallback face, so the bundled Noto Sans Arabic
#: is preferred there; on Windows it is registered by load_fonts() too.
_FONT_PREFERENCE_AR = ("Noto Sans Arabic", "Segoe UI", "DejaVu Sans",
                       "Tahoma", "Arial")

#: Bundled families, registered at start-up. Without these the Arabic pages
#: depend on whatever the host happens to ship, and a machine with no Arabic
#: font shows every Arabic label as empty boxes.
_BUNDLED_FONTS = ("NotoSansArabic-Regular.ttf", "NotoSansArabic-Bold.ttf",
                  "DejaVuSans.ttf")


def _assets_dir() -> str:
    """Where the bundled fonts live, in the source tree or inside the bundle."""
    import os
    import sys

    base = getattr(sys, "_MEIPASS", None)
    if base:
        bundled = os.path.join(base, "thesis_app", "assets", "fonts")
        if os.path.isdir(bundled):
            return bundled
    return os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "..", "assets", "fonts"))


def load_fonts() -> None:
    """Register the bundled fonts with Qt. Safe to call more than once."""
    import os

    directory = _assets_dir()
    for name in _BUNDLED_FONTS:
        path = os.path.join(directory, name)
        if os.path.isfile(path):
            QFontDatabase.addApplicationFont(path)


def _font_family() -> str:
    """First font in the direction-appropriate preference list that is installed."""
    available = set(QFontDatabase.families())
    order = _FONT_PREFERENCE_AR if _rtl() else _FONT_PREFERENCE
    for name in order:
        if name in available:
            return name
    return "sans-serif"


def base_font(size: int = 10) -> QFont:
    f = QFont(_font_family(), size)
    f.setStyleStrategy(QFont.PreferAntialias)
    return f


def letter_spacing() -> str:
    """Letter-spacing for small caps-style headings.

    Only Latin may be tracked. Arabic is a joined script: inserting space
    between letters breaks the joins and turns a word into a row of detached
    glyphs, so the property is dropped entirely in Arabic.
    """
    return "0px" if _rtl() else "1px"


def _rtl() -> bool:
    try:
        from .i18n import TRANSLATOR
        return bool(TRANSLATOR.is_rtl)
    except Exception:
        return False


def stylesheet() -> str:
    # Tracking is a Latin-only device; see letter_spacing().
    track = letter_spacing()
    track_wide = "0px" if _rtl() else "2px"
    stack = (_FONT_STACK_AR if _rtl() else _FONT_STACK)
    return f"""
* {{
    font-family: {stack};
    color: {TEXT};
}}

QWidget#Root {{
    background: {BG};
}}

/* ---------- sidebar ---------- */
QFrame#Sidebar {{
    background: {SURFACE};
    border-right: 1px solid {BORDER};
}}
QFrame#BrandBadge {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {HERO_A}, stop:1 {HERO_C});
    border-radius: 10px;
}}
QLabel#BrandBadgeText {{
    color: white;
    font-size: 13px;
    font-weight: 700;
}}
QLabel#Brand {{
    font-size: 14px;
    font-weight: 700;
    color: {TEXT};
}}
QLabel#BrandSub {{
    font-size: 10px;
    color: {TEXT_FAINT};
}}
QLabel#NavGroup {{
    font-size: 10px;
    font-weight: 700;
    color: {TEXT_FAINT};
    padding: 0 4px;
    letter-spacing: {track};
}}
QPushButton#NavItem {{
    text-align: left;
    padding: 8px 12px;
    border: none;
    border-radius: {RADIUS_SM};
    background: transparent;
    font-size: 12px;
    color: {TEXT_MUTED};
}}
QPushButton#NavItem:hover {{
    background: {SURFACE_2};
    color: {TEXT};
}}
QPushButton#NavItem:checked {{
    background: {ACCENT_SOFT};
    color: {ACCENT_DARK};
    font-weight: 700;
}}

/* ---------- header ---------- */
QFrame#Header {{
    background: {SURFACE};
    border-bottom: 1px solid {BORDER};
}}
QLabel#PageTitle {{
    font-size: 19px;
    font-weight: 700;
    color: {TEXT};
}}
QLabel#PageSub {{
    font-size: 12px;
    color: {TEXT_MUTED};
}}
QLabel#HeaderName {{
    font-size: 11px;
    color: {TEXT_FAINT};
}}

/* ---------- cards ---------- */
QFrame#Card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_LG};
}}
QFrame#CardFlat {{
    background: {SURFACE_2};
    border: 1px solid {BORDER};
    border-radius: {RADIUS};
}}
QLabel#CardTitle {{
    font-size: 14px;
    font-weight: 700;
    color: {TEXT};
}}
QLabel#CardHint {{
    font-size: 11px;
    color: {TEXT_MUTED};
}}
QLabel#Muted {{ color: {TEXT_MUTED}; font-size: 11px; }}
QLabel#Faint {{ color: {TEXT_FAINT}; font-size: 11px; }}
QLabel#Body {{ font-size: 12px; }}
QLabel#Lead {{
    font-size: 13px;
    color: {TEXT_MUTED};
}}
QLabel#BigValue {{ font-size: 22px; font-weight: 700; color: {ACCENT_DARK}; }}
QLabel#StatLabel {{ font-size: 11px; color: {TEXT_MUTED}; }}
QLabel#StatHint {{ font-size: 10px; color: {TEXT_FAINT}; }}

QPlainTextEdit#CodeView {{
    background: {SURFACE_2};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_SM};
    padding: 10px;
    color: {TEXT};
    selection-background-color: {ACCENT};
}}

/* ---------- hero banner ---------- */
QFrame#HeroCard {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {HERO_A}, stop:0.55 {HERO_B}, stop:1 {HERO_C});
    border: none;
    border-radius: 18px;
}}
QLabel#HeroKicker {{
    color: #c7d9ff;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: {track_wide};
}}
QLabel#HeroTitle {{
    color: white;
    font-size: 25px;
    font-weight: 700;
}}
QLabel#HeroSub {{
    color: #dbe7ff;
    font-size: 13px;
}}
QFrame#HeroRule {{
    background: rgba(255, 255, 255, 0.28);
    border: none;
    max-height: 1px;
    min-height: 1px;
}}
QLabel#HeroName {{
    color: white;
    font-size: 20px;
    font-weight: 700;
}}
QLabel#HeroMeta {{
    color: #dbe7ff;
    font-size: 12px;
}}
QLabel#HeroChip {{
    color: white;
    background: rgba(255, 255, 255, 0.16);
    border: 1px solid rgba(255, 255, 255, 0.30);
    border-radius: 11px;
    padding: 5px 12px;
    font-size: 11px;
    font-weight: 600;
}}

/* ---------- action cards ---------- */
QFrame#ActionCard {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_LG};
}}
QFrame#ActionCard:hover {{
    border: 1px solid {ACCENT_RING};
    background: {ACCENT_SOFT};
}}
QLabel#ActionIcon {{
    font-size: 20px;
}}
QLabel#ActionTitle {{
    font-size: 14px;
    font-weight: 700;
    color: {TEXT};
}}
QLabel#ActionBody {{
    font-size: 11px;
    color: {TEXT_MUTED};
}}

/* ---------- pills ---------- */
QLabel#Pill {{
    background: {SURFACE_2};
    color: {TEXT_MUTED};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 3px 10px;
    font-size: 10px;
    font-weight: 600;
}}
QLabel#PillAccent {{
    background: {ACCENT_SOFT};
    color: {ACCENT_DARK};
    border: 1px solid {ACCENT_RING};
    border-radius: 10px;
    padding: 3px 10px;
    font-size: 10px;
    font-weight: 600;
}}

/* ---------- step cards ---------- */
QFrame#StepCard {{
    background: {SURFACE_2};
    border: 1px solid {BORDER};
    border-radius: {RADIUS};
}}
QLabel#StepNum {{
    color: white;
    background: {ACCENT};
    border-radius: 11px;
    font-size: 11px;
    font-weight: 700;
}}
QLabel#StepTitle {{
    font-size: 12px;
    font-weight: 700;
    color: {TEXT};
}}
QLabel#StepBody {{
    font-size: 11px;
    color: {TEXT_MUTED};
}}

/* ---------- collapsible section ---------- */
QPushButton#SectionHead {{
    text-align: left;
    padding: 10px 14px;
    border: 1px solid {BORDER};
    border-radius: {RADIUS};
    background: {SURFACE};
    font-size: 13px;
    font-weight: 700;
    color: {TEXT};
}}
QPushButton#SectionHead:hover {{
    background: {SURFACE_2};
    border-color: {BORDER_STRONG};
}}
QFrame#SectionBody {{
    background: transparent;
    border: none;
}}

/* ---------- buttons ---------- */
QPushButton {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_SM};
    padding: 8px 15px;
    font-size: 12px;
}}
QPushButton:hover {{ background: {SURFACE_2}; border-color: {BORDER_STRONG}; }}
QPushButton:pressed {{ background: {SURFACE_3}; }}
QPushButton:disabled {{ color: {TEXT_FAINT}; background: {SURFACE_2}; }}
QPushButton#Primary {{
    background: {ACCENT};
    border: 1px solid {ACCENT};
    color: white;
    font-weight: 700;
    padding: 9px 18px;
}}
QPushButton#Primary:hover {{ background: {ACCENT_DARK}; border-color: {ACCENT_DARK}; }}
QPushButton#Primary:pressed {{ background: #1a44c2; }}
QPushButton#Primary:disabled {{ background: #9db8f2; border-color: #9db8f2; color: #eef2fb; }}
QPushButton#Ghost {{
    background: transparent;
    border: 1px solid {BORDER};
    color: {TEXT_MUTED};
}}
QPushButton#Ghost:hover {{ background: {SURFACE_2}; color: {TEXT}; }}
QPushButton#Quiet {{
    background: transparent;
    border: none;
    color: {TEXT_MUTED};
    padding: 6px 10px;
}}
QPushButton#Quiet:hover {{ color: {ACCENT_DARK}; background: {ACCENT_SOFT}; }}

/* ---------- inputs ---------- */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_SM};
    padding: 8px 10px;
    font-size: 12px;
    selection-background-color: {ACCENT};
}}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus,
QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
    border: 1px solid {ACCENT};
}}
QComboBox::drop-down {{ border: none; width: 22px; }}
QComboBox QAbstractItemView {{
    border: 1px solid {BORDER};
    background: {SURFACE};
    selection-background-color: {ACCENT_SOFT};
    selection-color: {TEXT};
    outline: none;
}}
QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{ width: 16px; }}

/* ---------- tables ---------- */
QTableWidget, QTableView {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_SM};
    gridline-color: {SURFACE_2};
    font-size: 12px;
}}
QHeaderView::section {{
    background: {SURFACE_2};
    border: none;
    border-bottom: 1px solid {BORDER};
    padding: 8px 10px;
    font-size: 11px;
    font-weight: 700;
    color: {TEXT_MUTED};
}}
QTableWidget::item {{ padding: 6px 8px; }}
QTableWidget::item:selected {{ background: {ACCENT_SOFT}; color: {TEXT}; }}

/* ---------- misc ---------- */
QProgressBar {{
    border: none;
    border-radius: 5px;
    background: {SURFACE_2};
    height: 10px;
    text-align: center;
    font-size: 10px;
    color: {TEXT_MUTED};
}}
QProgressBar::chunk {{ background: {ACCENT}; border-radius: 5px; }}
QScrollArea {{ border: none; background: transparent; }}
QScrollBar:vertical {{ background: transparent; width: 10px; margin: 0; }}
QScrollBar::handle:vertical {{ background: #ccd3dd; border-radius: 5px; min-height: 30px; }}
QScrollBar::handle:vertical:hover {{ background: #b3bcc9; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; width: 0; }}
QScrollBar::add-page, QScrollBar::sub-page {{ background: transparent; }}
QScrollBar:horizontal {{ background: transparent; height: 10px; margin: 0; }}
QScrollBar::handle:horizontal {{ background: #ccd3dd; border-radius: 5px; min-width: 30px; }}
QTabWidget::pane {{ border: 1px solid {BORDER}; border-radius: {RADIUS_SM}; background: {SURFACE}; top: -1px; }}
QTabBar::tab {{
    background: transparent;
    border: none;
    padding: 8px 16px;
    font-size: 12px;
    color: {TEXT_MUTED};
}}
QTabBar::tab:selected {{ color: {ACCENT_DARK}; font-weight: 700;
    border-bottom: 2px solid {ACCENT}; }}
QToolTip {{
    background: {TEXT};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 5px 8px;
    font-size: 11px;
}}
QSplitter::handle {{ background: {BORDER}; }}
"""


def badge_qss(kind: str) -> str:
    """Small pill style for a verdict badge."""
    if kind == "good":
        bg, fg = GOOD_SOFT, GOOD
    elif kind == "bad":
        bg, fg = BAD_SOFT, BAD
    else:
        bg, fg = WARN_SOFT, WARN
    return (f"background:{bg}; color:{fg}; border:1px solid {fg}33;"
            f"border-radius:8px; padding:7px 13px; font-weight:700;"
            f"font-size:12px;")
