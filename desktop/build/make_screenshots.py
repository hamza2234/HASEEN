#!/usr/bin/env python3
"""Regenerate every page screenshot in both languages.

    xvfb-run -a python build/make_screenshots.py

Writes ``docs/screenshots/<lang>-<page>.png`` for every page in ``NAV``. The
images are produced from the live application, so a screenshot always shows the
real chart data rather than a mock-up.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/thesis_app_mpl")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "docs", "screenshots")


def main() -> int:
    from PySide6.QtWidgets import QApplication

    from thesis_app.ui.i18n import TRANSLATOR
    from thesis_app.ui.main_window import NAV, MainWindow

    os.makedirs(OUT, exist_ok=True)
    app = QApplication.instance() or QApplication([])
    win = MainWindow()
    win.resize(1440, 960)
    win.show()

    # a short run so the experiment and results pages show real data
    from thesis_app.core import engine

    engine.run_experiment("spambase", n_pop=6, max_it=3, desired=46)

    written = []
    for lang in ("ar", "en"):
        TRANSLATOR.lang = lang
        app.processEvents()
        for key, _label, _cls in NAV:
            win.go(key)
            for _ in range(6):          # let charts finish drawing
                app.processEvents()
            path = os.path.join(OUT, f"{lang}-{key}.png")
            win.grab().save(path)
            written.append(path)
    print(f"wrote {len(written)} screenshots to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
