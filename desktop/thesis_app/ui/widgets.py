"""Small reusable widgets shared by the pages.

Kept intentionally plain: cards, statistic tiles, a scrollable page base, a
matplotlib canvas for the charts and a verdict banner.
"""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (QDialog, QFrame, QGridLayout, QHBoxLayout,
                               QLabel, QPlainTextEdit, QPushButton,
                               QScrollArea, QSizePolicy, QTableWidget,
                               QTableWidgetItem, QVBoxLayout, QWidget)

from . import theme


# --------------------------------------------------------------------------- #
#  Layout helpers                                                              #
# --------------------------------------------------------------------------- #
class Card(QFrame):
    """A white rounded panel with an optional title and hint line."""

    def __init__(self, title: str = "", hint: str = "", flat: bool = False,
                 parent=None):
        super().__init__(parent)
        self.setObjectName("CardFlat" if flat else "Card")
        self.body = QVBoxLayout(self)
        self.body.setContentsMargins(18, 16, 18, 16)
        self.body.setSpacing(10)
        self.title_label = None
        self.hint_label = None
        if title:
            self.title_label = QLabel(title)
            self.title_label.setObjectName("CardTitle")
            self.title_label.setWordWrap(True)
            self.body.addWidget(self.title_label)
        if hint:
            self.hint_label = QLabel(hint)
            self.hint_label.setObjectName("CardHint")
            self.hint_label.setWordWrap(True)
            self.body.addWidget(self.hint_label)

    def add(self, widget):
        self.body.addWidget(widget)
        return widget

    def add_layout(self, layout):
        self.body.addLayout(layout)
        return layout


class Page(QScrollArea):
    """Base class for every page: a scrollable column of cards."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        holder = QWidget()
        self.column = QVBoxLayout(holder)
        self.column.setContentsMargins(24, 20, 24, 28)
        self.column.setSpacing(16)
        self.setWidget(holder)

    def add(self, widget):
        self.column.addWidget(widget)
        return widget

    def add_card(self, title: str = "", hint: str = "", flat: bool = False):
        card = Card(title, hint, flat)
        self.column.addWidget(card)
        return card

    def stretch(self):
        self.column.addStretch(1)


def heading(text: str, sub: str = "") -> QWidget:
    box = QWidget()
    lay = QVBoxLayout(box)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(3)
    h = QLabel(text)
    f = h.font()
    f.setPointSize(f.pointSize() + 3)
    f.setBold(True)
    h.setFont(f)
    h.setWordWrap(True)
    lay.addWidget(h)
    if sub:
        s = QLabel(sub)
        s.setObjectName("Muted")
        s.setWordWrap(True)
        lay.addWidget(s)
    return box


def paragraph(text: str) -> QLabel:
    lab = QLabel(text)
    lab.setObjectName("Body")
    lab.setWordWrap(True)
    lab.setTextInteractionFlags(Qt.TextSelectableByMouse)
    return lab


def muted(text: str) -> QLabel:
    lab = QLabel(text)
    lab.setObjectName("Muted")
    lab.setWordWrap(True)
    return lab


def faint(text: str) -> QLabel:
    lab = QLabel(text)
    lab.setObjectName("Faint")
    lab.setWordWrap(True)
    return lab


def lead(text: str) -> QLabel:
    """A slightly larger introductory paragraph."""
    lab = QLabel(text)
    lab.setObjectName("Lead")
    lab.setWordWrap(True)
    lab.setTextInteractionFlags(Qt.TextSelectableByMouse)
    return lab


def pill(text: str, accent: bool = False) -> QLabel:
    lab = QLabel(text)
    lab.setObjectName("PillAccent" if accent else "Pill")
    lab.setAlignment(Qt.AlignCenter)
    return lab


def pill_row(items: list[str], accent: bool = False) -> QWidget:
    """A wrapping row of small chips."""
    box = QWidget()
    lay = QHBoxLayout(box)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(7)
    for text in items:
        lay.addWidget(pill(text, accent))
    lay.addStretch(1)
    return box


# --------------------------------------------------------------------------- #
#  Statistic tiles                                                             #
# --------------------------------------------------------------------------- #
class StatTile(QFrame):
    def __init__(self, label: str, value: str = "—", parent=None):
        super().__init__(parent)
        self.setObjectName("CardFlat")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(4)
        self.value_label = QLabel(value)
        self.value_label.setObjectName("BigValue")
        self.label_label = QLabel(label)
        self.label_label.setObjectName("StatLabel")
        self.label_label.setWordWrap(True)
        lay.addWidget(self.value_label)
        lay.addWidget(self.label_label)

    def set_value(self, value: str):
        self.value_label.setText(value)

    def set_label(self, label: str):
        self.label_label.setText(label)


def stat_row(tiles: list[StatTile]) -> QWidget:
    box = QWidget()
    lay = QHBoxLayout(box)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(12)
    for tile in tiles:
        lay.addWidget(tile)
    return box


def stat_grid(tiles: list[StatTile], columns: int = 3) -> QWidget:
    box = QWidget()
    grid = QGridLayout(box)
    grid.setContentsMargins(0, 0, 0, 0)
    grid.setSpacing(12)
    for i, tile in enumerate(tiles):
        grid.addWidget(tile, i // columns, i % columns)
    return box


# --------------------------------------------------------------------------- #
#  Hero banner                                                                 #
# --------------------------------------------------------------------------- #
class HeroBanner(QFrame):
    """The gradient header card used on the home page.

    Two columns: the thesis title on one side, the student's name on the other,
    separated by a hairline rule, with a row of chips underneath. Every string
    is settable, so the page can retranslate it in place instead of rebuilding
    the widget.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("HeroCard")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(30, 26, 30, 26)
        lay.setSpacing(0)

        # ---- top row: title block | rule | name block ---------------------
        top = QWidget()
        top_lay = QHBoxLayout(top)
        top_lay.setContentsMargins(0, 0, 0, 0)
        top_lay.setSpacing(26)

        left = QVBoxLayout()
        left.setContentsMargins(0, 0, 0, 0)
        left.setSpacing(0)
        self.kicker = QLabel("")
        self.kicker.setObjectName("HeroKicker")
        left.addWidget(self.kicker)
        left.addSpacing(9)
        self.title = QLabel("")
        self.title.setObjectName("HeroTitle")
        self.title.setWordWrap(True)
        left.addWidget(self.title)
        left.addSpacing(7)
        self.sub = QLabel("")
        self.sub.setObjectName("HeroSub")
        self.sub.setWordWrap(True)
        left.addWidget(self.sub)
        left.addStretch(1)
        top_lay.addLayout(left, 1)

        self.divider = QFrame()
        self.divider.setObjectName("HeroRule")
        self.divider.setFixedWidth(1)
        top_lay.addWidget(self.divider)

        right = QVBoxLayout()
        right.setContentsMargins(0, 0, 0, 0)
        right.setSpacing(0)
        right.addStretch(1)
        self.name_caption = QLabel("")
        self.name_caption.setObjectName("HeroMeta")
        right.addWidget(self.name_caption)
        right.addSpacing(4)
        self.name = QLabel("")
        self.name.setObjectName("HeroName")
        self.name.setWordWrap(True)
        self.name.setMinimumWidth(240)
        self.name.setMaximumWidth(340)
        self.name.setTextInteractionFlags(Qt.TextSelectableByMouse)
        right.addWidget(self.name)
        right.addSpacing(5)
        self.affiliation = QLabel("")
        self.affiliation.setObjectName("HeroMeta")
        self.affiliation.setWordWrap(True)
        self.affiliation.setMaximumWidth(340)
        right.addWidget(self.affiliation)
        right.addStretch(1)
        top_lay.addLayout(right)
        lay.addWidget(top)

        # ---- bottom: chips ------------------------------------------------
        lay.addSpacing(20)
        self.rule = QFrame()
        self.rule.setObjectName("HeroRule")
        self.rule.setFixedHeight(1)
        lay.addWidget(self.rule)
        lay.addSpacing(15)

        self.chip_holder = QWidget()
        self.chip_lay = QHBoxLayout(self.chip_holder)
        self.chip_lay.setContentsMargins(0, 0, 0, 0)
        self.chip_lay.setSpacing(8)
        lay.addWidget(self.chip_holder)

    def set_chips(self, items: list[str]):
        while self.chip_lay.count():
            item = self.chip_lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()
        for text in items:
            chip = QLabel(text)
            chip.setObjectName("HeroChip")
            self.chip_lay.addWidget(chip)
        self.chip_lay.addStretch(1)


# --------------------------------------------------------------------------- #
#  Action card                                                                 #
# --------------------------------------------------------------------------- #
class ActionCard(QFrame):
    """A clickable card: icon, title and one line of explanation.

    Used on the home page instead of a row of buttons, so the three things a
    visitor can do are self-describing rather than three unexplained labels.
    """

    def __init__(self, icon: str, title: str, body: str, on_click=None,
                 primary: bool = False, parent=None):
        super().__init__(parent)
        self.setObjectName("ActionCard")
        self.setCursor(Qt.PointingHandCursor)
        self._on_click = on_click
        self._primary = primary

        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 18, 20, 18)
        lay.setSpacing(9)

        self.icon_label = QLabel(icon)
        self.icon_label.setObjectName("ActionIcon")
        lay.addWidget(self.icon_label)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("ActionTitle")
        self.title_label.setWordWrap(True)
        lay.addWidget(self.title_label)

        self.body_label = QLabel(body)
        self.body_label.setObjectName("ActionBody")
        self.body_label.setWordWrap(True)
        lay.addWidget(self.body_label)
        lay.addStretch(1)

        self.cta = QLabel("")
        self.cta.setObjectName("PillAccent")
        self.cta.setAlignment(Qt.AlignCenter)
        self.cta.setMaximumWidth(140)
        lay.addWidget(self.cta, 0, Qt.AlignLeading)

    def set_texts(self, title: str, body: str, cta: str):
        self.title_label.setText(title)
        self.body_label.setText(body)
        self.cta.setText(cta)

    def mouseReleaseEvent(self, event):        # pragma: no cover - GUI only
        if self._on_click is not None and event.button() == Qt.LeftButton:
            self._on_click()
        super().mouseReleaseEvent(event)


# --------------------------------------------------------------------------- #
#  Step card                                                                   #
# --------------------------------------------------------------------------- #
def step_card(number: int, title: str, body: str) -> tuple[QFrame, QLabel, QLabel]:
    """A numbered explanation tile. Returns the frame plus its two labels so
    the caller can retranslate them."""
    box = QFrame()
    box.setObjectName("StepCard")
    lay = QVBoxLayout(box)
    lay.setContentsMargins(16, 14, 16, 14)
    lay.setSpacing(8)

    head = QWidget()
    hl = QHBoxLayout(head)
    hl.setContentsMargins(0, 0, 0, 0)
    hl.setSpacing(9)

    num = QLabel(str(number))
    num.setObjectName("StepNum")
    num.setFixedSize(22, 22)
    num.setAlignment(Qt.AlignCenter)

    title_label = QLabel(title)
    title_label.setObjectName("StepTitle")
    title_label.setWordWrap(True)

    hl.addWidget(num, 0, Qt.AlignTop)
    hl.addWidget(title_label, 1)
    lay.addWidget(head)

    body_label = QLabel(body)
    body_label.setObjectName("StepBody")
    body_label.setWordWrap(True)
    lay.addWidget(body_label)
    return box, title_label, body_label


# --------------------------------------------------------------------------- #
#  Collapsible section                                                         #
# --------------------------------------------------------------------------- #
class CollapsibleSection(QWidget):
    """A titled section that is collapsed by default.

    The long reference pages (datasets, algorithm, MATLAB) put their raw tables
    and source listings inside one of these, so the page opens short and the
    detail is one click away instead of scrolling past the reader.
    """

    def __init__(self, title: str, hint: str = "", expanded: bool = False,
                 parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        self.head = QPushButton(title)
        self.head.setObjectName("SectionHead")
        self.head.setCheckable(True)
        self.head.setChecked(expanded)
        self.head.setCursor(Qt.PointingHandCursor)
        self.head.clicked.connect(self._toggle)
        lay.addWidget(self.head)

        self.body_frame = QFrame()
        self.body_frame.setObjectName("SectionBody")
        self.body = QVBoxLayout(self.body_frame)
        self.body.setContentsMargins(16, 14, 16, 4)
        self.body.setSpacing(12)
        lay.addWidget(self.body_frame)

        self.hint = hint
        self._refresh()

    def _toggle(self):
        self._refresh()

    def _refresh(self):
        expanded = self.head.isChecked()
        self.body_frame.setVisible(expanded)
        marker = "▾" if expanded else "▸"
        text = self.head.text().lstrip("▾▸ ").strip()
        self.head.setText(f"{marker}  {text}")
        self.head.setProperty("expanded", expanded)

    def set_title(self, title: str):
        self.head.setProperty("_title", title)
        expanded = self.head.isChecked()
        marker = "▾" if expanded else "▸"
        self.head.setText(f"{marker}  {title}")

    def add(self, widget):
        self.body.addWidget(widget)
        return widget

    def add_layout(self, layout):
        self.body.addLayout(layout)
        return layout


# --------------------------------------------------------------------------- #
#  Key/value rows                                                              #
# --------------------------------------------------------------------------- #
def kv_rows(pairs: list[tuple[str, str]]) -> QWidget:
    box = QWidget()
    lay = QVBoxLayout(box)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(8)
    for key, val in pairs:
        row = QWidget()
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(12)
        k = QLabel(key)
        k.setObjectName("Muted")
        k.setMinimumWidth(190)
        k.setWordWrap(True)
        v = QLabel(str(val))
        v.setWordWrap(True)
        v.setTextInteractionFlags(Qt.TextSelectableByMouse)
        v.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        rl.addWidget(k)
        rl.addWidget(v, 1)
        lay.addWidget(row)
    return box


class KVBlock(QWidget):
    """A key/value list that can rebuild itself when the language changes.

    ``pairs_fn`` is a callable returning ``[(label, value), ...]``; it is
    re-invoked on every rebuild, so it can consult the active language.
    """

    def __init__(self, pairs_fn, parent=None):
        super().__init__(parent)
        self._pairs_fn = pairs_fn
        self._lay = QVBoxLayout(self)
        self._lay.setContentsMargins(0, 0, 0, 0)
        self._lay.setSpacing(8)
        self.rebuild()

    def rebuild(self):
        # unparent first: deleteLater() only runs when control returns to the
        # event loop, and until then the old rows would still be visible.
        while self._lay.count():
            item = self._lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()
        for key, val in self._pairs_fn():
            row = QWidget()
            rl = QHBoxLayout(row)
            rl.setContentsMargins(0, 0, 0, 0)
            rl.setSpacing(12)
            k = QLabel(key)
            k.setObjectName("Muted")
            k.setMinimumWidth(180)
            k.setWordWrap(True)
            v = QLabel(str(val))
            v.setWordWrap(True)
            v.setTextInteractionFlags(Qt.TextSelectableByMouse)
            v.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            rl.addWidget(k)
            rl.addWidget(v, 1)
            self._lay.addWidget(row)


# --------------------------------------------------------------------------- #
#  Tables                                                                      #
# --------------------------------------------------------------------------- #
def make_table(headers: list[str], rows: list[list], stretch_col: int = -1,
               max_height: int | None = None) -> QTableWidget:
    tbl = QTableWidget(len(rows), len(headers))
    tbl.setHorizontalHeaderLabels(headers)
    tbl.verticalHeader().setVisible(False)
    tbl.setEditTriggers(QTableWidget.NoEditTriggers)
    tbl.setSelectionBehavior(QTableWidget.SelectRows)
    tbl.setAlternatingRowColors(False)
    tbl.setShowGrid(False)
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            item = QTableWidgetItem("" if val is None else str(val))
            item.setTextAlignment(Qt.AlignCenter if c else Qt.AlignVCenter | Qt.AlignLeading)
            tbl.setItem(r, c, item)
    tbl.resizeColumnsToContents()
    hdr = tbl.horizontalHeader()
    if stretch_col >= 0:
        hdr.setStretchLastSection(False)
        tbl.setColumnWidth(stretch_col, max(tbl.columnWidth(stretch_col), 240))
        hdr.setSectionResizeMode(stretch_col, hdr.ResizeMode.Stretch)
    else:
        hdr.setStretchLastSection(True)
    if max_height:
        tbl.setMaximumHeight(max_height)
    return tbl


# --------------------------------------------------------------------------- #
#  Verdict banner                                                              #
# --------------------------------------------------------------------------- #
class VerdictBanner(QFrame):
    """Large colored result banner: green for real, red for fake."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CardFlat")
        lay = QHBoxLayout(self)
        lay.setContentsMargins(18, 16, 18, 16)
        lay.setSpacing(14)
        self.icon = QLabel("—")
        f = QFont()
        f.setPointSize(f.pointSize() + 12)
        self.icon.setFont(f)
        self.text = QLabel("")
        tf = QFont()
        tf.setPointSize(tf.pointSize() + 2)
        tf.setBold(True)
        self.text.setFont(tf)
        self.text.setWordWrap(True)
        self.sub = QLabel("")
        self.sub.setObjectName("Muted")
        self.sub.setWordWrap(True)
        col = QVBoxLayout()
        col.setContentsMargins(0, 0, 0, 0)
        col.setSpacing(3)
        col.addWidget(self.text)
        col.addWidget(self.sub)
        lay.addWidget(self.icon)
        lay.addLayout(col, 1)

    def show_verdict(self, is_fake: bool, title: str, sub: str = ""):
        if is_fake:
            bg, fg, icon = theme.BAD_SOFT, theme.BAD, "⚠"
        else:
            bg, fg, icon = theme.GOOD_SOFT, theme.GOOD, "✓"
        self.setStyleSheet(
            f"QFrame#CardFlat{{background:{bg}; border:1px solid {fg}44;"
            f"border-radius:10px;}}")
        self.icon.setText(icon)
        self.icon.setStyleSheet(f"color:{fg};")
        self.text.setText(title)
        self.text.setStyleSheet(f"color:{fg};")
        self.sub.setText(sub)

    def clear(self):
        self.setStyleSheet("")
        self.icon.setText("—")
        self.text.setText("")
        self.sub.setText("")


# --------------------------------------------------------------------------- #
#  Probability bars                                                            #
# --------------------------------------------------------------------------- #
class ProbBars(QWidget):
    """Two horizontal bars showing the class probabilities."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.setSpacing(8)

    def set_probs(self, names: list[str], probs: list[float]):
        while self.lay.count():
            item = self.lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()
        for name, p in zip(names, probs):
            row = QWidget()
            rl = QHBoxLayout(row)
            rl.setContentsMargins(0, 0, 0, 0)
            rl.setSpacing(10)
            lab = QLabel(name)
            lab.setMinimumWidth(120)
            lab.setObjectName("Muted")
            bar = QFrame()
            bar.setFixedHeight(10)
            bar.setStyleSheet(
                f"background:{theme.SURFACE_2}; border-radius:5px;")
            fill = QFrame(bar)
            fill.setStyleSheet(
                f"background:{theme.ACCENT}; border-radius:5px;")
            fill.setFixedHeight(10)
            bar.resize(200, 10)

            def _resize(event, b=bar, f=fill, p=p):
                f.setGeometry(0, 0, int(b.width() * max(0.0, min(1.0, p))),
                              b.height())
            bar.resizeEvent = _resize
            bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            pct = QLabel(f"{p * 100:.1f}%")
            pct.setMinimumWidth(58)
            pct.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            rl.addWidget(lab)
            rl.addWidget(bar, 1)
            rl.addWidget(pct)
            self.lay.addWidget(row)
        # trigger an initial layout pass
        self.resize(self.width(), self.height())


# --------------------------------------------------------------------------- #
#  Chart canvas                                                                #
# --------------------------------------------------------------------------- #
def chart_canvas(height: int = 240, width: int = 420):
    """Return (canvas_widget, figure). Imported lazily so matplotlib stays
    optional until a chart is actually needed."""
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
    from matplotlib.figure import Figure

    fig = Figure(figsize=(width / 100, height / 100), dpi=100,
                 facecolor=theme.SURFACE)
    canvas = FigureCanvasQTAgg(fig)
    canvas.setMinimumHeight(height)
    canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    return canvas, fig


def style_axes(ax, title: str = ""):
    ax.set_facecolor(theme.SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(theme.BORDER)
    ax.tick_params(colors=theme.TEXT_MUTED, labelsize=8)
    ax.grid(True, color=theme.BORDER, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    if title:
        ax.set_title(title, fontsize=10, color=theme.TEXT, pad=10)


# --------------------------------------------------------------------------- #
#  Thesis figures                                                              #
# --------------------------------------------------------------------------- #
class ImageTile(QFrame):
    """A thesis figure with a caption, scaled to fit and clickable to enlarge."""

    def __init__(self, path, caption: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("CardFlat")
        self._path = str(path)
        self._pixmap = QPixmap(self._path)
        self.setCursor(Qt.PointingHandCursor)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 12, 12, 12)
        lay.setSpacing(8)

        self.view = QLabel()
        self.view.setAlignment(Qt.AlignCenter)
        self.view.setMinimumHeight(200)
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if self._pixmap.isNull():
            self.view.setText("⚠")
        else:
            self.view.setPixmap(self._pixmap.scaled(
                520, 380, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        lay.addWidget(self.view)

        self.caption = QLabel(caption)
        self.caption.setObjectName("CardHint")
        self.caption.setWordWrap(True)
        self.caption.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.caption)

    def mouseReleaseEvent(self, event):        # pragma: no cover - GUI only
        if not self._pixmap.isNull():
            self._open_full()
        super().mouseReleaseEvent(event)

    def _open_full(self):
        dlg = QDialog(self)
        dlg.setWindowTitle(self.caption.text())
        dlg.resize(1000, 760)
        box = QVBoxLayout(dlg)
        area = QScrollArea(dlg)
        area.setWidgetResizable(True)
        pic = QLabel()
        pic.setPixmap(self._pixmap)
        pic.setAlignment(Qt.AlignCenter)
        area.setWidget(pic)
        box.addWidget(area)
        dlg.exec()


def image_grid(items: list, columns: int = 2) -> QWidget:
    """Lay :class:`ImageTile` widgets out in a grid."""
    holder = QWidget()
    grid = QGridLayout(holder)
    grid.setContentsMargins(0, 0, 0, 0)
    grid.setSpacing(12)
    for i, tile in enumerate(items):
        grid.addWidget(tile, i // columns, i % columns)
    for c in range(columns):
        grid.setColumnStretch(c, 1)
    return holder


# --------------------------------------------------------------------------- #
#  Source code                                                                 #
# --------------------------------------------------------------------------- #
def code_view(text: str, max_height: int = 380) -> QPlainTextEdit:
    """A read-only monospaced view of a source file."""
    box = QPlainTextEdit(text)
    box.setReadOnly(True)
    box.setLineWrapMode(QPlainTextEdit.NoWrap)
    font = QFont("Menlo")
    font.setStyleHint(QFont.Monospace)
    font.setPointSize(9)
    box.setFont(font)
    box.setMaximumHeight(max_height)
    box.setObjectName("CodeView")
    # source is always left-to-right, even in the Arabic layout
    box.setLayoutDirection(Qt.LeftToRight)
    return box
