"""Common base for the content pages."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPushButton

from ..i18n import t
from ..widgets import Card, CollapsibleSection, Page


class BasePage(Page):
    """A page whose text can be rebuilt when the language changes.

    Subclasses build the widget tree once in ``__init__`` (via ``build``).
    Any widget whose text comes from the string table must be created through
    the helpers below — :meth:`label`, :meth:`button`, :meth:`card` — which
    register the widget together with its key. The shell then calls
    :meth:`retranslate` whenever the language switches.

    Text that is computed rather than looked up (a number, a dataset name, a
    verdict) is not registered; subclasses refresh it by overriding
    :meth:`retranslate` and calling ``super().retranslate()`` first.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._texts: list[tuple] = []      # (widget, key, method)
        self.build()

    #: When True the page throws away its whole widget tree and runs
    #: :meth:`build` again on a language change. Set this for pages whose text
    #: is computed (``pick``, dataset fields, table rows) rather than looked up
    #: in the string table — rebuilding is less code than re-registering every
    #: individual piece. Pages that hold state worth keeping (a finished
    #: experiment, a verdict) leave this False and register their strings.
    rebuildable = False

    # -- subclass hooks ----------------------------------------------------
    def build(self):
        raise NotImplementedError

    def on_show(self):
        """Called each time the page becomes visible."""

    # -- retranslation -----------------------------------------------------
    def keep(self, widget, key, method: str = "setText"):
        """Register ``widget`` so ``method(...)`` is re-applied on a language
        change. ``key`` is either a string-table key or a zero-argument
        callable returning the text (for text that is built rather than looked
        up). Returns the widget for convenient chaining."""
        self._texts.append((widget, key, method))
        return widget

    def retranslate(self):
        if self.rebuildable:
            self.rebuild()
            return
        for widget, key, method in self._texts:
            text = key() if callable(key) else t(key)
            getattr(widget, method)(text)

    def rebuild(self):
        """Discard every widget in the page column and run :meth:`build`."""
        self._texts.clear()
        while self.column.count():
            item = self.column.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()
        self.build()

    @staticmethod
    def _clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()

    # -- translatable constructors -----------------------------------------
    def label(self, key: str, object_name: str = "", wrap: bool = False,
              parent=None) -> QLabel:
        """A ``QLabel`` bound to ``key`` in the string table."""
        lab = QLabel(t(key), parent)
        if object_name:
            lab.setObjectName(object_name)
        if wrap:
            lab.setWordWrap(True)
        return self.keep(lab, key)

    def button(self, key: str, object_name: str = "",
               parent=None) -> QPushButton:
        """A ``QPushButton`` bound to ``key`` in the string table."""
        btn = QPushButton(t(key), parent)
        if object_name:
            btn.setObjectName(object_name)
        btn.setCursor(Qt.PointingHandCursor)
        return self.keep(btn, key)

    def card(self, title_key: str = "", hint_key: str = "",
             flat: bool = False) -> Card:
        """A ``Card`` whose title and hint are bound to string-table keys."""
        card = Card(t(title_key) if title_key else "",
                    t(hint_key) if hint_key else "", flat)
        if title_key and card.title_label is not None:
            self.keep(card.title_label, title_key)
        if hint_key and card.hint_label is not None:
            self.keep(card.hint_label, hint_key)
        return card

    def add_card(self, title_key: str = "", hint_key: str = "",
                 flat: bool = False) -> Card:
        """Create a bound card and append it to the page column."""
        return self.add(self.card(title_key, hint_key, flat))

    def section(self, title_key: str, expanded: bool = False) -> CollapsibleSection:
        """A collapsible section bound to a string-table key.

        The detail lives inside it, so the page opens short and the reader
        chooses when to see the raw tables or listings.
        """
        sec = CollapsibleSection(t(title_key), expanded=expanded)
        sec.head.setProperty("_i18n_key", title_key)
        self.keep(sec, title_key, "set_title")
        return sec

    def add_section(self, title_key: str,
                    expanded: bool = False) -> CollapsibleSection:
        """Create a bound collapsible section and append it to the page."""
        return self.add(self.section(title_key, expanded))
