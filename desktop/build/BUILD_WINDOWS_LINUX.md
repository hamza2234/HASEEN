# Building the Windows release from Linux (Wine)

The thesis application must ship a real Windows build. PyInstaller cannot
cross-compile, so the Windows artefacts are produced by running a Windows
Python toolchain under Wine. This is the exact recipe that produced
`HybridPSOGA-Setup-1.0.0.exe` and `HybridPSOGA-Windows-Portable.zip`.

## Host packages

```bash
sudo dpkg --add-architecture i386 && sudo apt-get update
sudo apt-get install -y wine64 wine32:i386 xvfb imagemagick p7zip-full cabextract
```

The Python installer and Inno Setup are 32-bit bootstrappers, so `wine32` is
required even though everything we build is 64-bit.

## Wine prefix

```bash
export WINEPREFIX=/tmp/wp2 WINEARCH=win64 WINEDEBUG=-all XDG_RUNTIME_DIR=/tmp/xdgrt
mkdir -p /tmp/wp2 /tmp/xdgrt
Xvfb :99 -screen 0 1280x1024x24 &        # installers need a display, even /quiet
export DISPLAY=:99
wineboot --init
```

## Windows Python and the pinned dependency set

```bash
curl -LO https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe
wine python-3.12.8-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 \
     Include_test=0 TargetDir=C:\\Py312
```

Versions matter. These are the newest releases that still run under Wine:

| package        | version | why it is pinned |
|----------------|---------|------------------|
| numpy          | 1.26.4  | 2.x ships an OpenBLAS that calls `crealf`, which Wine's `ucrtbase` stubs and aborts on |
| pandas         | 2.2.3   | last release compatible with numpy 1.26 |
| scikit-learn   | 1.5.2   | matches the numpy 1.x ABI |
| scipy          | 1.13.1  | matches the numpy 1.x ABI |
| matplotlib     | 3.9.2   | matches the numpy 1.x ABI |
| PySide6-Essentials, shiboken6 | 6.6.3.1 | 6.7+ links `icuuc.dll`, which the wheel does not ship; 6.6.3.1 bundles the MSVC runtime it needs |
| pyinstaller    | 6.22.3  | build tool |

```bash
wine C:\\Py312\\python.exe -m pip install \
  "numpy==1.26.4" "pandas==2.2.3" "scikit-learn==1.5.2" "scipy==1.13.1" \
  "matplotlib==3.9.2" "PySide6-Essentials==6.6.3.1" "shiboken6==6.6.3.1" \
  openpyxl pyinstaller
```

## Build

Copy the sources into the prefix, then run the same commands a Windows
developer would run (see `build_windows.bat`):

```bash
mkdir -p /tmp/wp2/drive_c/app
cp -r thesis_app run_app.py verify_app.py build /tmp/wp2/drive_c/app/
cp -r docs /tmp/wp2/drive_c/app/
cd /tmp/wp2/drive_c/app

wine C:\\Py312\\python.exe run_app.py --selftest          # must print SELFTEST OK
wine C:\\Py312\\python.exe verify_app.py                  # must print 71 passed, 0 failed
wine C:\\Py312\\python.exe -m PyInstaller build\\thesis_app.spec --noconfirm
```

`dist\HybridPSOGA\HybridPSOGA.exe` is the frozen application.

## Installer

```bash
curl -LO https://github.com/jrsoftware/issrc/releases/download/is-6_7_4/innosetup-6.7.4.exe
wine innosetup-6.7.4.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-
wine "C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe" build\\installer.iss
```

Output: `build\Output\HybridPSOGA-Setup-1.0.0.exe`.

The portable archive is just a ZIP of `dist\HybridPSOGA\`.

## Verifying the result

```bash
wine dist/HybridPSOGA/HybridPSOGA.exe --selftest
wine build/Output/HybridPSOGA-Setup-1.0.0.exe /VERYSILENT /SUPPRESSMSGBOXES \
     /NORESTART /SP- /DIR=C:\\InstalledApp
wine C:\\InstalledApp\\HybridPSOGA.exe --selftest
```

All three must report `SELFTEST OK: 0 problem(s)`.

## Caveat

Wine proves the build is a valid Windows PE binary that loads and runs, and
that the bundled data and models are intact. It is not a substitute for a
smoke test on real Windows: the frozen `.exe` carries the real MSVC runtime
and links against the genuine Windows UCRT at load time, so it must still be
launched once on an actual Windows machine before the release is published.
