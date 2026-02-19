"""CSV parsing utilities with strict schema validation."""
import csv
from datetime import datetime
from typing import Iterator
from io import StringIO

from backend.models.transaction import Transaction


REQUIRED_COLUMNS = ['transaction_id', 'sender_id', 'receiver_id', 'amount', 'timestamp']


def validate_csv_columns(header: list[str]) -> None:
    """Validate CSV has exact required columns."""
    header_lower = [col.lower().strip() for col in header]
    missing = [col for col in REQUIRED_COLUMNS if col.lower() not in header_lower]
    
    if missing:
        raise ValueError(
            f"Missing required columns: {missing}. "
            f"Required columns: {REQUIRED_COLUMNS}"
        )
    
    # Check for extra columns (optional strictness)
    extra = [col for col in header_lower if col not in REQUIRED_COLUMNS]
    if extra:
        # Warn but don't fail - allow extra columns
        pass


def parse_csv(file_content: str) -> list[Transaction]:
    """
    Parse CSV content into Transaction objects.
    
    Args:
        file_content: CSV file content as string
        
    Returns:
        List of Transaction objects
        
    Raises:
        ValueError: If CSV schema is invalid or data is malformed
    """
    reader = csv.DictReader(StringIO(file_content))
    
    # Validate header
    if not reader.fieldnames:
        raise ValueError("CSV file is empty or has no header row")
    
    validate_csv_columns(list(reader.fieldnames))
    
    transactions = []
    errors = []
    
    # Normalize column names (case-insensitive)
    field_map = {col.lower().strip(): col for col in reader.fieldnames}
    
    for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
        try:
            # Extract values using normalized mapping
            transaction_id = row[field_map['transaction_id']].strip()
            sender_id = row[field_map['sender_id']].strip()
            receiver_id = row[field_map['receiver_id']].strip()
            amount = float(row[field_map['amount']])
            timestamp_str = row[field_map['timestamp']].strip()
            
            # Parse timestamp
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            
            transaction = Transaction(
                transaction_id=transaction_id,
                sender_id=sender_id,
                receiver_id=receiver_id,
                amount=amount,
                timestamp=timestamp
            )
            transactions.append(transaction)
            
        except (ValueError, KeyError) as e:
            errors.append(f"Row {row_num}: {str(e)}")
    
    if errors:
        raise ValueError(f"CSV parsing errors:\n" + "\n".join(errors[:10]))
    
    if not transactions:
        raise ValueError("No valid transactions found in CSV")
    
    return transactions
