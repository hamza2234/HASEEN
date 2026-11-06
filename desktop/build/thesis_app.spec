# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller specification for the desktop application.

Build on Windows with:

    pyinstaller build/thesis_app.spec --noconfirm

The result is a single folder ``dist/HybridPSOGA/`` containing
``HybridPSOGA.exe``. That folder is what the installer wraps. Everything -
the two datasets and the eight thesis figures - is bundled, so the application
never needs a network connection.
"""
import os

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# the project root (the folder that contains thesis_app/ and run_app.py)
ROOT = os.path.dirname(os.path.abspath(SPECPATH))
ASSETS = os.path.join(ROOT, "thesis_app", "assets")


def _data(rel, dest="thesis_app/assets"):
    return (os.path.join(ASSETS, rel), dest)


datas = [
    _data("data/spambase.xlsx", "thesis_app/assets/data"),
    _data("data/Data_phishing.xlsx", "thesis_app/assets/data"),
    _data("figures", "thesis_app/assets/figures"),
    _data("matlab", "thesis_app/assets/matlab"),
    _data("main.m"),
    _data("GA_PSO_feature_selection.m"),
    _data("fitness_RF.m"),
    _data("repair_solution.m"),
    _data("plot_results.m"),
]

# matplotlib needs its style and font data files
datas += collect_data_files("matplotlib")

hiddenimports = (
    collect_submodules("sklearn")
    + collect_submodules("matplotlib.backends")
    + ["pandas", "numpy", "openpyxl", "PySide6.QtSvg"]
)

block_cipher = None

a = Analysis(
    [os.path.join(ROOT, "run_app.py")],
    pathex=[ROOT],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter", "PyQt5", "PyQt6", "PySide2", "IPython", "notebook",
        "jupyter", "pytest", "sphinx", "torch", "tensorflow", "cv2",
        # Qt modules the application never touches
        "PySide6.QtWebEngineCore", "PySide6.QtWebEngineWidgets",
        "PySide6.QtWebEngineQuick", "PySide6.QtQuick", "PySide6.QtQuick3D",
        "PySide6.QtQml", "PySide6.Qt3DCore", "PySide6.Qt3DRender",
        "PySide6.QtCharts", "PySide6.QtDataVisualization",
        "PySide6.QtMultimedia", "PySide6.QtMultimediaWidgets",
        "PySide6.QtBluetooth", "PySide6.QtNfc", "PySide6.QtPositioning",
        "PySide6.QtSql", "PySide6.QtTest", "PySide6.QtDesigner",
        "PySide6.QtHelp", "PySide6.QtSerialPort", "PySide6.QtWebSockets",
        "PySide6.QtWebChannel", "PySide6.QtRemoteObjects",
        "PySide6.QtSensors", "PySide6.QtSpatialAudio",
        "PySide6.QtStateMachine", "PySide6.QtPdf", "PySide6.QtPdfWidgets",
        # heavy data payloads we do not ship
        "scipy.io.tests", "scipy.sparse.tests",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="HybridPSOGA",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,          # GUI application: no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="HybridPSOGA",
)
