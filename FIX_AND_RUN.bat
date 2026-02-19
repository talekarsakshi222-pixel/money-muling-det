@echo off
echo ========================================
echo FIXING AND STARTING SERVERS
echo ========================================
echo.

cd /d %~dp0

REM Step 1: Create venv if needed
if not exist venv (
    echo [1/5] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Cannot create venv. Check Python installation.
        pause
        exit /b 1
    )
    echo Virtual environment created.
) else (
    echo [1/5] Virtual environment exists.
)
echo.

REM Step 2: Activate and install backend
echo [2/5] Installing backend dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet
python -m pip install fastapi uvicorn[standard] python-multipart pydantic networkx python-dateutil
if errorlevel 1 (
    echo ERROR: Backend install failed!
    pause
    exit /b 1
)
echo Backend dependencies installed.
echo.

REM Step 3: Install frontend
echo [3/5] Installing frontend dependencies...
cd frontend
if not exist node_modules (
    call npm install
    if errorlevel 1 (
        echo ERROR: Frontend install failed!
        cd ..
        pause
        exit /b 1
    )
) else (
    echo Frontend dependencies already installed.
)
cd ..
echo.

REM Step 4: Verify installations
echo [4/5] Verifying installations...
venv\Scripts\python.exe -c "import fastapi, networkx, pydantic; print('Backend: OK')" 2>&1
if errorlevel 1 (
    echo WARNING: Backend packages may not be installed correctly
)
if exist frontend\node_modules (
    echo Frontend: OK
) else (
    echo WARNING: Frontend dependencies missing
)
echo.

REM Step 5: Start servers
echo [5/5] Starting servers...
echo.
echo Opening backend server window...
start "Money Muling - Backend" cmd /k "cd /d %~dp0 && venv\Scripts\activate.bat && echo Backend starting on http://localhost:8000 && python backend/main.py"

timeout /t 4 /nobreak >nul

echo Opening frontend server window...
start "Money Muling - Frontend" cmd /k "cd /d %~dp0\frontend && echo Frontend starting on http://localhost:5173 && npm run dev"

echo.
echo ========================================
echo SERVERS ARE STARTING!
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Two windows opened - DO NOT CLOSE THEM
echo Wait 10-15 seconds, then open:
echo   http://localhost:5173
echo.
echo Press any key to close this window...
echo ========================================
pause >nul
