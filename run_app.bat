@echo off
chcp 65001 >nul
title kopo - Streamlit Dashboard
cd /d "%~dp0"

REM ===== Writable folders inside the project =====
set "HOME_DIR=%~dp0_userhome"
set "CFG_DIR=%~dp0.streamlit"
if not exist "%HOME_DIR%" mkdir "%HOME_DIR%"
if not exist "%CFG_DIR%"  mkdir "%CFG_DIR%"

REM ===== Redirect user/streamlit folders to avoid Windows permission errors =====
set "HOME=%HOME_DIR%"
set "USERPROFILE=%HOME_DIR%"
set "STREAMLIT_CONFIG_DIR=%CFG_DIR%"
set "STREAMLIT_BROWSER_GATHER_USAGE_STATS=false"

echo ================================================================
echo   kopo Dashboard - Data Mining Project
echo   Project : %~dp0
echo   HOME    : %HOME%
echo ================================================================
echo.

streamlit run app.py --server.headless true --server.port 8501 --server.address 127.0.0.1 --browser.gatherUsageStats false
pause
