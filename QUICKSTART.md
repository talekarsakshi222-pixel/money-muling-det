# Quick Start Guide

## Prerequisites Check

```bash
# Check Python version (need 3.9+)
python --version

# Check Node.js version (need 18+)
node --version
npm --version
```

## Installation Steps

### 1. Backend Setup (Terminal 1)

```bash
# Navigate to project root
cd d:\money-mulling-det

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install Python dependencies
pip install -r requirements.txt

# Start backend server
python backend/main.py
```

Backend should be running at `http://localhost:8000`

### 2. Frontend Setup (Terminal 2)

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start development server
npm run dev
```

Frontend should be running at `http://localhost:5173`

## Testing

1. Open browser to `http://localhost:5173`
2. Upload the sample CSV file: `sample_transactions.csv`
3. View detection results:
   - Graph visualization
   - Fraud ring table
   - Detection summary
4. Download JSON results

## API Testing

```bash
# Health check
curl http://localhost:8000/api/health

# Upload CSV
curl -X POST -F "file=@sample_transactions.csv" http://localhost:8000/api/detect
```

## Troubleshooting

### Backend Issues

**Import errors**: Make sure you're running from project root directory
```bash
cd d:\money-mulling-det
python backend/main.py
```

**Port already in use**: Change port in `backend/main.py`
```python
uvicorn.run(..., port=8001)
```

### Frontend Issues

**Module not found**: Run `npm install` in frontend directory

**CORS errors**: Check that backend CORS settings in `backend/api/main.py` include your frontend URL

**Graph not rendering**: Check browser console for Cytoscape errors

## Next Steps

- Review `README.md` for detailed documentation
- Check algorithm explanations in code comments
- Customize detection parameters in `backend/services/` files
- Adjust scoring weights in `backend/services/scoring.py`
