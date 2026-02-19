"""Smurfing detection: fan-in and fan-out patterns."""
from datetime import datetime, timedelta
from typing import TYPE_CHECKING
from collections import defaultdict

if TYPE_CHECKING:
    from networkx import DiGraph
    from backend.models.transaction import Transaction


def detect_smurfing(
    G: 'DiGraph',
    transactions: list['Transaction'],
    threshold: int = 10,
    time_window_hours: int = 72
) -> dict[str, dict]:
    """
    Detect smurfing patterns: fan-in and fan-out.
    
    Fan-in: >=threshold unique senders → 1 receiver within time_window
    Fan-out: 1 sender → >=threshold receivers within time_window
    
    Complexity: O(n) where n = number of transactions
    Uses timestamp filtering and aggregation
    
    Args:
        G: Directed graph
        transactions: Original transaction list for timestamp filtering
        threshold: Minimum number of connections (default: 10)
        time_window_hours: Time window in hours (default: 72)
        
    Returns:
        Dictionary mapping account_id to detection info:
        {
            'account_id': str,
            'pattern_type': 'fan_in' | 'fan_out',
            'pattern_label': str,
            'count': int,
            'time_window_start': datetime,
            'time_window_end': datetime
        }
    """
    results: dict[str, dict] = {}
    
    # Build time-indexed transaction map for efficient filtering
    # Group by receiver (fan-in) and sender (fan-out)
    receiver_tx_map: dict[str, list['Transaction']] = defaultdict(list)
    sender_tx_map: dict[str, list['Transaction']] = defaultdict(list)
    
    for tx in transactions:
        receiver_tx_map[tx.receiver_id].append(tx)
        sender_tx_map[tx.sender_id].append(tx)
    
    # Detect fan-in patterns
    for receiver_id, tx_list in receiver_tx_map.items():
        # Sort by timestamp
        tx_list_sorted = sorted(tx_list, key=lambda t: t.timestamp)
        
        # Sliding window approach
        for i, start_tx in enumerate(tx_list_sorted):
            window_start = start_tx.timestamp
            window_end = window_start + timedelta(hours=time_window_hours)
            
            # Count unique senders in window
            unique_senders = set()
            for tx in tx_list_sorted[i:]:
                if tx.timestamp > window_end:
                    break
                unique_senders.add(tx.sender_id)
            
            if len(unique_senders) >= threshold:
                results[receiver_id] = {
                    'account_id': receiver_id,
                    'pattern_type': 'fan_in',
                    'pattern_label': f'fan_in_{threshold}_{time_window_hours}h',
                    'count': len(unique_senders),
                    'time_window_start': window_start,
                    'time_window_end': window_end
                }
                break  # Found pattern, move to next receiver
    
    # Detect fan-out patterns
    for sender_id, tx_list in sender_tx_map.items():
        # Skip if already detected as fan-in
        if sender_id in results:
            continue
            
        tx_list_sorted = sorted(tx_list, key=lambda t: t.timestamp)
        
        # Sliding window approach
        for i, start_tx in enumerate(tx_list_sorted):
            window_start = start_tx.timestamp
            window_end = window_start + timedelta(hours=time_window_hours)
            
            # Count unique receivers in window
            unique_receivers = set()
            for tx in tx_list_sorted[i:]:
                if tx.timestamp > window_end:
                    break
                unique_receivers.add(tx.receiver_id)
            
            if len(unique_receivers) >= threshold:
                results[sender_id] = {
                    'account_id': sender_id,
                    'pattern_type': 'fan_out',
                    'pattern_label': f'fan_out_{threshold}_{time_window_hours}h',
                    'count': len(unique_receivers),
                    'time_window_start': window_start,
                    'time_window_end': window_end
                }
                break  # Found pattern, move to next sender
    
    return results
