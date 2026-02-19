# Installation Guide

## Issue: Pydantic Core Compilation Error

If you're encountering Rust/Cargo errors when installing pydantic, it's because Python 3.13 requires newer package versions with pre-built wheels.

## Solution: Use Virtual Environment

### Step 1: Create Virtual Environment

```bash
# Navigate to project directory
cd d:\money-mulling-det

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### Step 2: Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Step 3: Install Dependencies

**Option A: Install latest compatible versions (Recommended)**
```bash
pip install fastapi uvicorn[standard] python-multipart pydantic networkx python-dateutil
```

**Option B: Use requirements.txt with wheel-only install**
```bash
pip install --only-binary :all: -r requirements.txt
```

**Option C: If Option B fails, install individually**
```bash
pip install fastapi
pip install "uvicorn[standard]"
pip install python-multipart
pip install pydantic
pip install networkx
pip install python-dateutil
```

### Step 4: Verify Installation

```bash
python -c "import fastapi, networkx, pydantic; print('All packages installed successfully!')"
```

## Alternative: Use Python 3.11 or 3.12

If you continue having issues with Python 3.13, consider using Python 3.11 or 3.12, which have better package compatibility:

1. Install Python 3.11 or 3.12
2. Create virtual environment with that version:
   ```bash
   py -3.11 -m venv venv
   # or
   py -3.12 -m venv venv
   ```
3. Follow steps above

## Quick Setup Script (Windows)

Run the provided `setup_backend.bat` script:
```bash
setup_backend.bat
```

This will automatically:
- Create virtual environment
- Activate it
- Upgrade pip
- Install all dependencies
