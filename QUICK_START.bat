@echo off
cls
echo ========================================
echo MONEY MULING DETECTION ENGINE
echo Quick Start Script
echo ========================================
echo.

cd /d %~dp0

REM Activate venv
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment activated
) else (
    echo [ERROR] Virtual environment not found!
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing backend packages...
    pip install fastapi uvicorn[standard] python-multipart pydantic networkx python-dateutil
)

REM Check backend packages
venv\Scripts\python.exe -c "import fastapi" 2>nul
if errorlevel 1 (
    echo [INSTALL] Installing backend packages...
    pip install fastapi uvicorn[standard] python-multipart pydantic networkx python-dateutil
) else (
    echo [OK] Backend packages ready
)

REM Check frontend
cd frontend
if not exist node_modules (
    echo [INSTALL] Installing frontend packages (this takes 1-2 minutes)...
    call npm install
) else (
    echo [OK] Frontend packages ready
)
cd ..

echo.
echo ========================================
echo STARTING SERVERS...
echo ========================================
echo.

REM Start backend
echo [STARTING] Backend server on http://localhost:8000
start "Backend - Money Muling" cmd /k "cd /d %~dp0 && venv\Scripts\activate.bat && python backend/main.py"

REM Wait
timeout /t 3 /nobreak >nul

REM Start frontend  
echo [STARTING] Frontend server on http://localhost:5173
start "Frontend - Money Muling" cmd /k "cd /d %~dp0\frontend && npm run dev"

echo.
echo ========================================
echo SERVERS STARTING!
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Two windows will open - DO NOT CLOSE THEM
echo Wait 15 seconds, then open browser to:
echo   http://localhost:5173
echo ========================================
echo.
timeout /t 10
