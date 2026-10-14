@echo off
echo ========================================================
echo Secret Communication System - Windows Automated Setup
echo ========================================================

python --version
if errorlevel 1 (
    echo Python is not installed or not in PATH! Please install Python 3.11 or 3.12.
    pause
    exit /b 1
)

echo.
echo [1/4] Installing Required Dependencies...
pip install -r requirements.txt
pip install email-validator

echo.
echo [2/4] Setting Up Environment Configuration...
if not exist .env (
    copy .env.example .env
    echo Created .env from .env.example
) else (
    echo .env already exists.
)

echo.
echo [3/4] Initializing Database and Demo Data...
python scripts\generate_demo_data.py

echo.
echo [4/4] Running Automated Test Suite...
python -m pytest tests

echo.
echo ========================================================
echo Setup Completed Successfully!
echo To start the web server run: run_windows.bat or python run.py
echo ========================================================
pause
