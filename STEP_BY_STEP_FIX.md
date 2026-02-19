# Step-by-Step Fix - Follow Exactly

## The Problem
- Backend dependencies not installed (fastapi, etc.)
- Frontend dependencies not installed (node_modules missing)
- Servers can't start without dependencies

## Solution - Do This Now:

### OPTION 1: Use the Fix Script (Easiest)

1. **Double-click this file**: `FIX_AND_RUN.bat`
2. Wait for it to finish (it will open 2 windows)
3. Wait 15 seconds
4. Open browser to: `http://localhost:5173`

---

### OPTION 2: Manual Fix (If script doesn't work)

#### Terminal 1 - Backend Setup:

```powershell
# Navigate to project
cd d:\money-mulling-det

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1
# If that fails, try:
# venv\Scripts\activate.bat

# Install backend packages
pip install fastapi uvicorn[standard] python-multipart pydantic networkx python-dateutil

# Start backend (KEEP THIS TERMINAL OPEN)
python backend/main.py
```

You should see: `Uvicorn running on http://0.0.0.0:8000`

#### Terminal 2 - Frontend Setup:

```powershell
# Navigate to frontend
cd d:\money-mulling-det\frontend

# Install dependencies (takes 1-2 minutes)
npm install

# Start frontend (KEEP THIS TERMINAL OPEN)
npm run dev
```

You should see: `Local: http://localhost:5173`

#### Step 3: Open Browser

Go to: **http://localhost:5173**

---

## Verify It's Working

### Check Backend:
Open: http://localhost:8000/api/health
Should show: `{"status":"healthy"}`

### Check Frontend:
Open: http://localhost:5173
Should show: Upload CSV interface

---

## Common Issues

### "python: command not found"
- Install Python from python.org
- Make sure Python is in PATH

### "npm: command not found"  
- Install Node.js from nodejs.org
- Restart terminal after installing

### "Permission denied" errors
- Use virtual environment (venv) - this fixes it
- Don't use `sudo` or admin mode

### Port already in use
```powershell
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <number> /F

# Kill process on port 5173  
netstat -ano | findstr :5173
taskkill /PID <number> /F
```

---

## Still Not Working?

1. Make sure you have TWO terminal windows open (one for backend, one for frontend)
2. Make sure BOTH are running (you should see server output)
3. Wait 10-15 seconds after starting before opening browser
4. Check Windows Firewall isn't blocking ports
