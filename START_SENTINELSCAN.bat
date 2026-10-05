@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
title SentinelScan Launcher

set "ROOT=%~dp0"
set "DATA=%ROOT%data"
set "PORT=8000"
set "PY="
set "PYEXE="

cls
echo ============================================================
echo                 SENTINELSCAN LAUNCHER
echo ============================================================
echo.

REM ------------------------------------------------------------
REM 1. Find a usable Python installation. No FINDSTR is used.
REM ------------------------------------------------------------
echo [1/4] Checking Python...
where py >nul 2>nul
if not errorlevel 1 (
    set "PY=py"
    for /f "delims=" %%V in ('py --version 2^>^&1') do set "PYVER=%%V"
    goto PYTHON_OK
)
where python >nul 2>nul
if not errorlevel 1 (
    set "PY=python"
    for /f "delims=" %%V in ('python --version 2^>^&1') do set "PYVER=%%V"
    goto PYTHON_OK
)

echo [ERROR] Python was not found.
echo Install Python 3.11+ and enable "Add Python to PATH", then run this again.
pause
exit /b 1

:PYTHON_OK
echo        !PYVER!

REM ------------------------------------------------------------
REM 2. Prepare writable project data. No admin rights required.
REM ------------------------------------------------------------
echo [2/4] Preparing SentinelScan data...
if not exist "%DATA%" mkdir "%DATA%" >nul 2>&1
if not exist "%DATA%\security_state.json" (
    >"%DATA%\security_state.json" echo {"lab_fixed":false,"findings":{},"history":[]}
)
if not exist "%DATA%\security_state.json" (
    echo [ERROR] Cannot write to:
    echo         %DATA%
    echo Try extracting SentinelScan into a folder you can write to, such as Documents or Desktop.
    pause
    exit /b 1
)

REM This build uses Python standard library only; no pip/venv is required.
REM If a local .venv already exists and works, it is intentionally ignored so
REM Windows permission problems with .venv never block the launcher.
set "SENTINELSCAN_DATA=%DATA%"

REM ------------------------------------------------------------
REM 3. Start server, then wait for the actual health endpoint.
REM ------------------------------------------------------------
echo [3/4] Starting SentinelScan server...
start "SentinelScan Server" "%ROOT%run_server.bat"

echo        Waiting for server at http://127.0.0.1:%PORT%/health ...
set "READY=0"
for /L %%I in (1,1,30) do (
    %PY% -c "from urllib.request import urlopen; r=urlopen('http://127.0.0.1:%PORT%/health',timeout=1); raise SystemExit(0 if r.status==200 else 1)" >nul 2>&1
    if not errorlevel 1 (
        set "READY=1"
        goto SERVER_READY
    )
    timeout /t 1 /nobreak >nul
)

if "!READY!"=="0" (
    echo.
    echo [ERROR] SentinelScan server did not become ready within 30 seconds.
    echo Check the "SentinelScan Server" window for the Python error.
    echo.
    echo Do NOT open frontend\index.html directly.
    pause
    exit /b 1
)

:SERVER_READY
echo        Server is READY.

REM ------------------------------------------------------------
REM 4. Open the dashboard only after the backend is ready.
REM ------------------------------------------------------------
echo [4/4] Opening SentinelScan dashboard...
start "" "http://127.0.0.1:%PORT%/"
echo.
echo ============================================================
echo SentinelScan is running.
echo Open Security Center and click RUN SECURITY ASSESSMENT.
echo Keep the SentinelScan Server window open while testing.
echo ============================================================
echo.
endlocal
exit /b 0
