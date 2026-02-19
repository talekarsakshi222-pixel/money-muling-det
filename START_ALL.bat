@echo off
echo ========================================
echo Money Muling Detection Engine
echo Complete Setup and Start Script
echo ========================================
echo.

REM Check Python
echo [1/4] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.9+
    pause
    exit /b 1
)
echo.

REM Setup Backend
echo [2/4] Setting up Backend...
cd backend
python -m pip install --upgrade pip --quiet
python -m pip install fastapi uvicorn[standard] python-multipart pydantic networkx python-dateutil --quiet
if errorlevel 1 (
    echo ERROR: Backend dependencies failed to install
    echo Trying with requirements.txt...
    cd ..
    python -m pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo ERROR: Backend setup failed!
        pause
        exit /b 1
    )
) else (
    echo Backend dependencies installed successfully
)
cd ..
echo.

REM Setup Frontend
echo [3/4] Setting up Frontend...
cd frontend
if not exist node_modules (
    echo Installing frontend dependencies (this may take a minute)...
    call npm install --silent
    if errorlevel 1 (
        echo ERROR: Frontend dependencies failed to install
        pause
        exit /b 1
    )
) else (
    echo Frontend dependencies already installed
)
cd ..
echo.

REM Start Backend
echo [4/4] Starting servers...
echo.
echo Starting BACKEND on http://localhost:8000
start "Backend Server" cmd /k "cd /d %~dp0 && python backend/main.py"

timeout /t 3 /nobreak >nul

echo Starting FRONTEND on http://localhost:5173
start "Frontend Server" cmd /k "cd /d %~dp0\frontend && npm run dev"

echo.
echo ========================================
echo Servers are starting!
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Two new windows will open for the servers.
echo Close this window when done.
echo ========================================
timeout /t 5
