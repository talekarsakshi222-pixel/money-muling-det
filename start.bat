@echo off
title Money Muling Detection Engine
color 0A
cls

echo.
echo ========================================
echo   MONEY MULING DETECTION ENGINE
echo   Starting Application...
echo ========================================
echo.

cd /d %~dp0

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.9+
    pause
    exit /b 1
)

REM Check Node
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found! Please install Node.js 18+
    pause
    exit /b 1
)

echo [1/4] Setting up backend...

REM Create venv if needed
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install backend packages if needed
venv\Scripts\python.exe -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo Installing backend packages...
    venv\Scripts\python.exe -m pip install --upgrade pip --quiet
    venv\Scripts\python.exe -m pip install fastapi uvicorn[standard] python-multipart pydantic networkx python-dateutil --quiet
    if errorlevel 1 (
        echo [ERROR] Backend installation failed!
        pause
        exit /b 1
    )
    echo Backend packages installed.
) else (
    echo Backend packages ready.
)

echo.
echo [2/4] Setting up frontend...

cd frontend

REM Install frontend packages if needed
if not exist node_modules (
    echo Installing frontend packages (this may take 1-2 minutes)...
    call npm install --silent
    if errorlevel 1 (
        echo [ERROR] Frontend installation failed!
        cd ..
        pause
        exit /b 1
    )
    echo Frontend packages installed.
) else (
    echo Frontend packages ready.
)

cd ..

echo.
echo [3/4] Starting backend server...
start "Money Muling - Backend" cmd /k "cd /d %~dp0 && venv\Scripts\activate.bat && echo Backend Server - DO NOT CLOSE THIS WINDOW && echo. && python backend/main.py"

timeout /t 4 /nobreak >nul

echo [4/4] Starting frontend server...
start "Money Muling - Frontend" cmd /k "cd /d %~dp0\frontend && echo Frontend Server - DO NOT CLOSE THIS WINDOW && echo. && npm run dev"

echo.
echo ========================================
echo   SERVERS STARTING!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Two windows opened - DO NOT CLOSE THEM
echo.
echo Wait 10-15 seconds, then open your browser:
echo   http://localhost:5173
echo.
echo Press any key to close this window...
echo ========================================
pause >nul
