@echo off
title Money Muling Detection - Starting...
cls
color 0B

echo.
echo ========================================
echo   MONEY MULING DETECTION ENGINE
echo   Complete Startup Script
echo ========================================
echo.

cd /d %~dp0

REM Step 1: Setup Backend
echo [STEP 1/4] Backend Setup...
if not exist venv (
    echo   Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat >nul 2>&1
venv\Scripts\python.exe -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo   Installing backend packages...
    venv\Scripts\python.exe -m pip install --upgrade pip --quiet
    venv\Scripts\python.exe -m pip install fastapi uvicorn[standard] python-multipart pydantic networkx python-dateutil --quiet
)
echo   [OK] Backend ready

REM Step 2: Setup Frontend
echo [STEP 2/4] Frontend Setup...
cd frontend
if not exist node_modules (
    echo   Installing frontend packages (1-2 min)...
    call npm install --silent
)
cd ..
echo   [OK] Frontend ready

REM Step 3: Start Backend
echo [STEP 3/4] Starting Backend Server...
start "Money Muling - Backend" cmd /k "cd /d %~dp0 && title Backend Server && venv\Scripts\activate.bat && echo ======================================== && echo   BACKEND SERVER && echo   http://localhost:8000 && echo ======================================== && echo. && python backend/main.py"
timeout /t 3 /nobreak >nul

REM Step 4: Start Frontend
echo [STEP 4/4] Starting Frontend Server...
start "Money Muling - Frontend" cmd /k "cd /d %~dp0\frontend && title Frontend Server && echo ======================================== && echo   FRONTEND SERVER && echo   http://localhost:5173 && echo ======================================== && echo. && npm run dev"

echo.
echo ========================================
echo   SERVERS STARTED!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Two windows opened - DO NOT CLOSE THEM
echo.
echo Wait 10-15 seconds, then open:
echo   http://localhost:5173
echo.
echo Press any key to close this window...
pause >nul
