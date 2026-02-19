@echo off
echo Starting Frontend Development Server...
echo.

cd frontend

REM Check if node_modules exists
if not exist node_modules (
    echo Dependencies not found. Installing...
    call npm install
)

echo Starting Vite dev server on http://localhost:5173
call npm run dev
