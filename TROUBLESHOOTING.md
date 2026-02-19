# Troubleshooting Guide

## Issue: Nothing is Working

### Problem 1: Backend Dependencies Not Installed

**Symptoms:**
- `ModuleNotFoundError: No module named 'fastapi'`
- Backend server won't start

**Solution:**
Use a virtual environment to avoid permission issues:

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn[standard] python-multipart pydantic networkx python-dateutil
```

### Problem 2: Frontend Dependencies Not Installed

**Symptoms:**
- `ERR_CONNECTION_REFUSED` on localhost:5173
- No `node_modules` folder

**Solution:**
```bash
cd frontend
npm install
npm run dev
```

### Problem 3: Permission Errors

**Symptoms:**
- `Permission denied` errors during pip install
- `OSError: [Errno 13] Permission denied`

**Solution:**
ALWAYS use a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
pip install ...
```

### Problem 4: Port Already in Use

**Symptoms:**
- `Address already in use`
- Server won't start

**Solution:**
```bash
# Find and kill process on port 8000 (backend)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Find and kill process on port 5173 (frontend)
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

## Quick Fix: Use the Setup Script

Run the provided script:
```bash
SETUP_AND_RUN.bat
```

This will:
1. Create virtual environment
2. Install all dependencies
3. Start both servers

## Manual Setup Steps

### Backend:
```bash
# 1. Create and activate venv
python -m venv venv
venv\Scripts\activate

# 2. Install packages
pip install fastapi uvicorn[standard] python-multipart pydantic networkx python-dateutil

# 3. Start server
python backend/main.py
```

### Frontend:
```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start server
npm run dev
```

## Verify Installation

### Check Backend:
```bash
python -c "import fastapi, networkx, pydantic; print('OK')"
```

### Check Frontend:
```bash
cd frontend
if exist node_modules (echo OK) else (echo Missing)
```

## Still Having Issues?

1. Make sure Python 3.9+ is installed
2. Make sure Node.js 18+ is installed
3. Try using Python 3.11 or 3.12 instead of 3.13
4. Check firewall/antivirus isn't blocking ports
5. Run commands as administrator if needed
