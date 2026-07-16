@echo off
REM =================================================
REM OpenRefine Reconciliation Toolkit
REM START_RECONCILIATION_SERVICES.bat
REM
REM Starts:
REM   - Library of Congress Reconciliation Service
REM   - Canadian Subject Headings Reconciliation Service
REM
REM Toolkit Version: 1.1.0
REM =================================================

title OpenRefine Reconciliation Toolkit Launcher v1.1.0
cls

echo.
echo Starting OpenRefine Reconciliation Toolkit v1.1.0...
echo.
cd /d "%~dp0"

IF NOT EXIST "venv\Scripts\activate.bat" (
    echo ERROR: Toolkit virtual environment not found.
    echo.
    echo Please run INSTALL_TOOLKIT.bat first.
    echo.
    pause
    exit /b 1
)

echo Starting CSH reconciliation service on http://localhost:5001/reconcile
start "CSH Reconciliation Service" cmd /k "cd /d "%~dp0csh-service" && call "%~dp0venv\Scripts\activate.bat" && csv-reconcile serve"


echo Starting LoC reconciliation service on http://localhost:5000/reconcile/LoC
start "LoC Reconciliation Service" cmd /k "cd /d "%~dp0loc-service" && call "%~dp0venv\Scripts\activate.bat" && python LoCreconcile.py"

timeout /t 2 >nul

echo.
echo =================================================
echo OpenRefine Reconciliation Toolkit
echo =================================================
echo.
echo The following services are now running:
echo.
echo Library of Congress (LCNAF/LCSH)
echo http://localhost:5000/reconcile/LoC
echo.
echo Canadian Subject Headings (CSH)
echo http://localhost:5001/reconcile
echo.
echo You may now open OpenRefine.
echo.
echo Press any key to close this window...
pause