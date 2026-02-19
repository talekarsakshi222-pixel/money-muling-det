@echo off
echo ========================================
echo Money Muling Detection Engine
echo Complete Setup and Run Script
echo ========================================
echo.

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install backend dependencies
echo Installing backend dependencies...
python -m pip install fastapi uvicorn[standard] python-multipart pydantic networkx python-dateutil
if errorlevel 1 (
    echo ERROR: Backend dependencies installation failed
    pause
    exit /b 1
)
echo Backend dependencies installed!
echo.

REM Setup Frontend
echo Installing frontend dependencies...
cd frontend
if not exist node_modules (
    call npm install
    if errorlevel 1 (
        echo ERROR: Frontend dependencies installation failed
        cd ..
        pause
        exit /b 1
    )
)
cd ..
echo Frontend dependencies installed!
echo.

REM Start Backend
echo ========================================
echo Starting BACKEND server...
echo Backend will run at: http://localhost:8000
echo ========================================
start "Backend Server" cmd /k "cd /d %~dp0 && venv\Scripts\activate.bat && python backend/main.py"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start Frontend
echo ========================================
echo Starting FRONTEND server...
echo Frontend will run at: http://localhost:5173
echo ========================================
start "Frontend Server" cmd /k "cd /d %~dp0\frontend && npm run dev"

echo.
echo ========================================
echo Setup Complete!
echo.
echo Two new windows opened:
echo   - Backend:  http://localhost:8000
echo   - Frontend: http://localhost:5173
echo.
echo Open your browser to: http://localhost:5173
echo ========================================
echo.
pause
