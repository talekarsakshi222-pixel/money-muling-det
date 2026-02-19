"""Suspicion scoring system."""
from typing import TYPE_CHECKING
from collections import defaultdict

if TYPE_CHECKING:
    from networkx import DiGraph
    from backend.models.transaction import Transaction


# Scoring weights per design spec:
# - Cycle detection: +40 points (same for all lengths)
# - Smurfing detection: +30 points
# - Shell detection: +25 points (per pattern)
# - High velocity: +15 points

SCORE_CYCLE_LENGTH_3 = 40
SCORE_CYCLE_LENGTH_4 = 40
SCORE_CYCLE_LENGTH_5 = 40
SCORE_SMURFING = 30
SCORE_SHELL_3_HOP = 25
SCORE_SHELL_4_HOP = 25
SCORE_SHELL_5_HOP = 25
SCORE_HIGH_VELOCITY = 15

# Velocity thresholds
HIGH_VELOCITY_THRESHOLD = 50  # transactions per day
PAYROLL_PATTERN_THRESHOLD = 0.8  # similarity threshold for payroll patterns


def calculate_suspicion_scores(
    G: 'DiGraph',
    transactions: list['Transaction'],
    cycle_accounts: dict[str, list[list[str]]],
    smurfing_accounts: dict[str, dict],
    shell_accounts: dict[str, list[list[str]]],
    account_ring_map: dict[str, str]
) -> dict[str, float]:
    """
    Calculate suspicion scores for all accounts.
    
    Scoring model:
    - Cycle detection: +40 points
    - Smurfing detection: +30 points
    - Shell detection: +25 points
    - High velocity: +15 points (if not payroll pattern)
    
    Scores are capped at 100.
    
    Complexity: O(n) where n = number of accounts
    
    Args:
        G: Transaction graph
        transactions: Original transaction list
        cycle_accounts: Accounts involved in cycles (ring_id -> cycles)
        smurfing_accounts: Accounts with smurfing patterns
        shell_accounts: Accounts involved in shells (ring_id -> chains)
        account_ring_map: Mapping of account_id -> ring_id
        
    Returns:
        Dictionary mapping account_id to suspicion_score
    """
    from collections import defaultdict

    scores: dict[str, float] = defaultdict(float)

    # Build unique pattern list for each account
    account_patterns: dict[str, set[str]] = defaultdict(set)

    # Cycle patterns
    for ring_id, cycles in cycle_accounts.items():
        for cycle in cycles:
            pattern_label = f"cycle_length_{len(cycle)}"
            for account_id in cycle:
                account_patterns[account_id].add(pattern_label)

    # Smurfing patterns
    for account_id, info in smurfing_accounts.items():
        label = info.get("pattern_label", "smurfing")
        account_patterns[account_id].add(label)

    # Shell patterns
    for ring_id, chains in shell_accounts.items():
        for chain in chains:
            pattern_label = f"layered_shell_{len(chain)}hop"
            for account_id in chain:
                account_patterns[account_id].add(pattern_label)

    # Score based on unique patterns
    for account_id, patterns in account_patterns.items():
        for label in patterns:
            if label.startswith("cycle_length_"):
                try:
                    length = int(label.split("_")[-1])
                except ValueError:
                    length = 3
                if length == 3:
                    scores[account_id] += SCORE_CYCLE_LENGTH_3
                elif length == 4:
                    scores[account_id] += SCORE_CYCLE_LENGTH_4
                else:
                    scores[account_id] += SCORE_CYCLE_LENGTH_5
            elif label.startswith("layered_shell_"):
                # extract hop count
                hop_str = label.replace("layered_shell_", "").replace("hop", "")
                try:
                    hop = int(hop_str)
                except ValueError:
                    hop = 3
                if hop == 3:
                    scores[account_id] += SCORE_SHELL_3_HOP
                elif hop == 4:
                    scores[account_id] += SCORE_SHELL_4_HOP
                else:
                    scores[account_id] += SCORE_SHELL_5_HOP
            elif label == "smurfing":
                scores[account_id] += SCORE_SMURFING
            # other patterns could be added here

    # Score high velocity (if not payroll pattern)
    velocity_scores = _calculate_velocity_scores(transactions)
    for account_id, velocity_score in velocity_scores.items():
        if not _is_payroll_pattern(account_id, transactions):
            scores[account_id] += velocity_score

    # Cap scores at 100
    for account_id in scores:
        scores[account_id] = min(scores[account_id], 100.0)

    return dict(scores)


def _calculate_velocity_scores(transactions: list['Transaction']) -> dict[str, float]:
    """
    Calculate velocity-based scores.
    
    High velocity: Many transactions in short time period.
    """
    from collections import defaultdict
    from datetime import timedelta
    
    account_tx_map: dict[str, list['Transaction']] = defaultdict(list)
    
    for tx in transactions:
        account_tx_map[tx.sender_id].append(tx)
        account_tx_map[tx.receiver_id].append(tx)
    
    velocity_scores: dict[str, float] = {}
    
    for account_id, tx_list in account_tx_map.items():
        if len(tx_list) < HIGH_VELOCITY_THRESHOLD:
            continue
        
        # Check transactions per day
        tx_list_sorted = sorted(tx_list, key=lambda t: t.timestamp)
        time_span = (tx_list_sorted[-1].timestamp - tx_list_sorted[0].timestamp).total_seconds() / 86400
        
        if time_span == 0:
            time_span = 1  # Avoid division by zero
        
        tx_per_day = len(tx_list) / time_span
        
        if tx_per_day >= HIGH_VELOCITY_THRESHOLD:
            velocity_scores[account_id] = SCORE_HIGH_VELOCITY
    
    return velocity_scores


def _is_payroll_pattern(account_id: str, transactions: list['Transaction']) -> bool:
    """
    Detect payroll-style patterns (repetitive monthly transactions).
    
    This helps avoid flagging legitimate high-volume accounts.
    """
    from collections import defaultdict
    
    # Get transactions involving this account
    account_txs = [
        tx for tx in transactions
        if tx.sender_id == account_id or tx.receiver_id == account_id
    ]
    
    if len(account_txs) < 10:
        return False
    
    # Group by month
    monthly_counts: dict[str, int] = defaultdict(int)
    for tx in account_txs:
        month_key = tx.timestamp.strftime('%Y-%m')
        monthly_counts[month_key] += 1
    
    if len(monthly_counts) < 3:
        return False
    
    # Check if counts are similar (payroll pattern)
    counts = list(monthly_counts.values())
    avg_count = sum(counts) / len(counts)
    
    # Calculate coefficient of variation
    if avg_count == 0:
        return False
    
    variance = sum((c - avg_count) ** 2 for c in counts) / len(counts)
    std_dev = variance ** 0.5
    cv = std_dev / avg_count if avg_count > 0 else 1.0
    
    # Low coefficient of variation indicates regular pattern
    return cv < 0.3  # Threshold for regularity
