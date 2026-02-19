"""Quick test script to verify backend works."""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from backend.models.transaction import Transaction
    from backend.utils.csv_parser import parse_csv
    from backend.services.detection_engine import run_detection
    
    print("[OK] All imports successful!")
    print("[OK] Backend is ready to run!")
    
    # Test CSV parsing
    test_csv = """transaction_id,sender_id,receiver_id,amount,timestamp
TXN_001,ACC_001,ACC_002,1000.00,2024-01-15 10:00:00
TXN_002,ACC_002,ACC_003,2000.00,2024-01-15 11:00:00"""
    
    transactions = parse_csv(test_csv)
    print(f"[OK] CSV parsing works! Parsed {len(transactions)} transactions")
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
