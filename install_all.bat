@echo off
echo Installing all dependencies...
echo.

cd /d %~dp0

echo [Backend] Creating virtual environment...
if not exist venv (
    python -m venv venv
)

echo [Backend] Installing Python packages...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet
python -m pip install fastapi uvicorn[standard] python-multipart pydantic networkx python-dateutil

echo.
echo [Frontend] Installing Node packages...
cd frontend
call npm install
cd ..

echo.
echo Installation complete!
echo Now run: start.bat
pause
