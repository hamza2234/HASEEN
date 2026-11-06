"""Application entry point."""
from __future__ import annotations

import os
import sys

# keep matplotlib from writing a cache inside a read-only install directory
os.environ.setdefault("MPLCONFIGDIR", os.path.join(
    os.environ.get("TEMP", "/tmp"), "thesis_app_mpl"))

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication


def _selftest() -> int:
    """Headless check used to confirm a frozen build found its bundled data."""
    from .core import engine, text_analyzer, url_analyzer

    failures = []
    for key in ("spambase", "phishing"):
        X, y, _ = engine.load_raw(key)
        cfg = engine.THESIS[key]
        ok = X.shape[0] == cfg["n_samples"] and X.shape[1] == cfg["n_features"]
        print(f"  {'PASS' if ok else 'FAIL'}  {key}: {X.shape[0]}x{X.shape[1]}")
        if not ok:
            failures.append(key)

    v = engine.predict_raw(
        "spambase",
        text_analyzer.extract_spambase_features(
            "URGENT verify your credit card and password now, free money!"))
    ok = bool(v["is_fake"])
    print(f"  {'PASS' if ok else 'FAIL'}  spam text -> fake")
    if not ok:
        failures.append("spam")

    vec, _ = url_analyzer.feature_vector("https://www.paypal.com/signin")
    v = engine.predict_raw("phishing", vec)
    ok = not v["is_fake"]
    print(f"  {'PASS' if ok else 'FAIL'}  paypal.com -> real")
    if not ok:
        failures.append("url")

    print(f"SELFTEST {'OK' if not failures else 'FAILED'}: "
          f"{len(failures)} problem(s)")
    return 1 if failures else 0


def main(argv=None) -> int:
    argv = list(sys.argv if argv is None else argv)

    if "--selftest" in argv:
        return _selftest()

    from .ui import theme
    from .ui.main_window import MainWindow

    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(argv)
    app.setApplicationName("Hybrid PSO-GA Feature Selection System")
    app.setApplicationDisplayName(
        "Hybrid PSO-GA Feature Selection System")
    app.setOrganizationName("Damghan University")
    app.setApplicationVersion("1.0.0")
    app.setStyle("Fusion")
    app.setFont(theme.base_font(10))

    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
