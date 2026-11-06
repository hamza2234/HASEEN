@echo off
REM ===================================================================
REM  One-click build for Windows: creates the .exe and then the setup
REM  file. Run this file by double-clicking it.
REM
REM  Requirements on the build machine (only the build machine):
REM    - Python 3.10 or newer, with "Add python.exe to PATH" ticked
REM    - Inno Setup 6 (https://jrsoftware.org/isdl.php)  [optional; the
REM      .exe is produced without it, only the installer needs it]
REM ===================================================================
setlocal
cd /d "%~dp0.."

echo.
echo [1/5] Checking Python...
python --version || (echo Python not found. Install it from python.org and tick "Add python.exe to PATH". & pause & exit /b 1)

echo.
echo [2/5] Installing the libraries (needs internet on this build machine only)...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt || (echo Library install failed. & pause & exit /b 1)

echo.
echo [3/5] Running the self-test...
python run_app.py --selftest || (echo Self-test failed. & pause & exit /b 1)

echo.
echo [4/5] Building the application folder (this takes 1-3 minutes)...
python -m PyInstaller build\thesis_app.spec --noconfirm || (echo Build failed. & pause & exit /b 1)
echo      Built: dist\HybridPSOGA\HybridPSOGA.exe

echo.
echo [5/5] Building the installer...
where iscc >nul 2>&1
if %errorlevel%==0 (
    iscc build\installer.iss
    echo      Installer: build\Output\HybridPSOGA-Setup-1.0.0.exe
) else (
    echo      Inno Setup not found, skipping the installer.
    echo      Install it from https://jrsoftware.org/isdl.php and run:
    echo          iscc build\installer.iss
    echo      Meanwhile dist\HybridPSOGA\HybridPSOGA.exe is ready to use.
)

echo.
echo ===================================================================
echo  Done.
echo ===================================================================
pause
