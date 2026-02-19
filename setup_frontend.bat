@echo off
echo Setting up frontend environment...
echo.

cd frontend

echo Installing npm dependencies...
call npm install

echo.
echo Frontend setup complete!
echo To start the dev server, run: npm run dev
echo Or use: run_frontend.bat

pause
