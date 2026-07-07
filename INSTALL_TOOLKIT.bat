@echo off
title OpenRefine Reconciliation Toolkit Installer
cls

echo.
echo ===============================================
echo OpenRefine Reconciliation Toolkit
echo Installer
echo ===============================================
echo.

cd /d "%~dp0"

echo Checking for Python...
python --version >nul 2>&1

IF ERRORLEVEL 1 (
    echo.
    echo =================================================
    echo Python was not found.
    echo =================================================
    echo.
    echo The OpenRefine Reconciliation Toolkit requires
    echo Python 3.x to be installed before installation.
    echo.
    echo Your web browser will now open the Python
    echo download page.
    echo.
    echo During installation, be sure to select:
    echo.
    echo     Add python.exe to PATH
    echo.
    echo After Python has been installed, run
    echo INSTALL_TOOLKIT.bat again.
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

IF EXIST "venv" (
    echo Existing virtual environment found.
    echo Skipping virtual environment creation.
) ELSE (
    echo Creating virtual environment...
    python -m venv venv

    IF ERRORLEVEL 1 (
        echo.
        echo ERROR: Could not create the virtual environment.
        pause
        exit /b 1
    )
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate

IF ERRORLEVEL 1 (
    echo.
    echo ERROR: Could not activate the virtual environment.
    pause
    exit /b 1
)

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

IF ERRORLEVEL 1 (
    echo.
    echo ERROR: pip upgrade failed.
    pause
    exit /b 1
)

echo.
echo Installing required packages...
pip install -r requirements.txt

IF ERRORLEVEL 1 (
    echo.
    echo ERROR: Package installation failed.
    pause
    exit /b 1
)

echo.
echo ===============================================
echo Installation complete.
echo ===============================================
echo Next step:
echo.
echo Double-click START_RECONCILIATION_SERVICES.bat
echo to start the reconciliation services.

pause