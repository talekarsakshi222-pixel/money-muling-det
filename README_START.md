# 🚀 START THE APPLICATION

## EASIEST WAY - Just Double-Click:

**`start.bat`** - This will:
- ✅ Check Python and Node.js
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Start both servers
- ✅ Open browser automatically

---

## Manual Start (If batch file doesn't work):

### Terminal 1 - Backend:
```bash
cd d:\money-mulling-det
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn[standard] python-multipart pydantic networkx python-dateutil
python backend/main.py
```

### Terminal 2 - Frontend:
```bash
cd d:\money-mulling-det\frontend
npm install
npm run dev
```

### Then Open Browser:
Go to: **http://localhost:5173**

---

## Test Backend:
```bash
python test_backend.py
```

---

## Troubleshooting:

**"Python not found"**
- Install Python from python.org
- Make sure it's in PATH

**"Node not found"**
- Install Node.js from nodejs.org
- Restart terminal after installing

**"Port already in use"**
```bash
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <number> /F

# Kill process on port 5173
netstat -ano | findstr :5173
taskkill /PID <number> /F
```

**"Module not found" errors**
- Make sure you're using the virtual environment
- Run: `venv\Scripts\activate` before starting backend
