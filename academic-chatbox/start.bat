@echo off
echo ========================================
echo Academic Chatbox - Quick Start
echo ========================================
echo.

echo [1/3] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.x
    pause
    exit /b 1
)

echo.
echo [2/3] Installing dependencies...
pip install -q flask

echo.
echo [3/3] Starting Flask server...
echo.
echo ========================================
echo Server will start at: http://127.0.0.1:5000
echo ========================================
echo.
echo Login Credentials:
echo   Admin:   admin / admin123
echo   Student: student / student123
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py
