@echo off
setlocal
cd /d "%~dp0"
set "SENTINELSCAN_DATA=%~dp0data"
if not exist "%SENTINELSCAN_DATA%" mkdir "%SENTINELSCAN_DATA%"
where py >nul 2>nul
if not errorlevel 1 (
  py backend\server.py
) else (
  python backend\server.py
)
pause
endlocal
