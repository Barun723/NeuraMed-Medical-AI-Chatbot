@echo off
title NeuraMed — AI Medical Intelligence
color 0A

:: ============================================================
::  NeuraMed Launcher  —  Double-click to start the app
::  Waits for Flask to be ready before opening the browser
:: ============================================================

echo.
echo  ============================================================
echo     NeuraMed  --  Where Intelligence Meets Care
echo     Built with heart by Mihir
echo  ============================================================
echo.

:: ── Always run from the folder this .bat lives in ──────────
cd /d "%~dp0"

:: ── Pick Python: venv first, then system ───────────────────
set "PYTHON=%~dp0mihu\Scripts\python.exe"

if not exist "%PYTHON%" (
    echo  [!!]  mihu venv not found — trying system Python...
    set "PYTHON=python"
)

:: ── Verify Python is usable ────────────────────────────────
"%PYTHON%" --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [ERROR] Python not found.
    echo          Make sure the mihu virtual environment exists, or
    echo          that Python is installed and on your PATH.
    echo.
    pause
    exit /b 1
)

echo  [OK]  Python found
echo  [..] Launching Flask server on http://localhost:5000 ...
echo  [..] Browser will open automatically once server is ready.
echo.
echo  Press Ctrl+C to stop the server.
echo  ============================================================
echo.

:: ── Start the browser-opener in a separate window ──────────
::    Uses PowerShell to poll until port 5000 is open,
::    then opens the browser (tries Chrome first, falls back to default). Timeout: 60 seconds.
start "" powershell -NoProfile -WindowStyle Hidden -Command "$url = 'http://localhost:5000'; $max = 120; $i = 0; while ($i -lt $max) { try { $tcp = New-Object System.Net.Sockets.TcpClient; $tcp.Connect('127.0.0.1', 5000); $tcp.Close(); try { Start-Process 'chrome' $url -ErrorAction Stop } catch { Start-Process $url }; exit 0 } catch {} Start-Sleep -Milliseconds 500; $i++ }"

:: ── Load GROQ_API_KEY from .env if present ────────────────
if exist .env (
    for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
        if "%%A"=="GROQ_API_KEY" (
            set "RAW_KEY=%%B"
            setlocal enabledelayedexpansion
            set "STRIP_KEY=!RAW_KEY:'=!"
            set "STRIP_KEY=!STRIP_KEY:"=!"
            for /f "tokens=1 delims=# " %%C in ("!STRIP_KEY!") do (
                endlocal
                set "GROQ_API_KEY=%%C"
            )
        )
    )
)

:: ── Run Flask (blocks — keeps this window as the log) ──────
"%PYTHON%" -m app.application

:: ── Only reaches here when Flask stops ─────────────────────
echo.
echo  ============================================================
echo  [--] NeuraMed server has stopped.
echo  ============================================================
echo.
pause
