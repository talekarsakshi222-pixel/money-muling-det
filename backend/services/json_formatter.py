"""JSON output formatter with exact schema matching."""
from typing import TYPE_CHECKING
from collections import defaultdict

if TYPE_CHECKING:
    from backend.models.transaction import Transaction, DetectionResult
    from networkx import DiGraph


def format_detection_result(
    G: 'DiGraph',
    transactions: list['Transaction'],
    cycle_accounts: dict[str, list[list[str]]],
    smurfing_accounts: dict[str, dict],
    shell_accounts: dict[str, list[list[str]]],
    suspicion_scores: dict[str, float],
    account_ring_map: dict[str, str],
    processing_time: float
) -> 'DetectionResult':
    """
    Format detection results into exact JSON schema.
    
    Schema:
    {
        "suspicious_accounts": [
            {
                "account_id": str,
                "suspicion_score": float (0-100),
                "detected_patterns": list[str],
                "ring_id": str | null
            }
        ],
        "fraud_rings": [
            {
                "ring_id": str,
                "member_accounts": list[str],
                "pattern_type": str,
                "risk_score": float (0-100)
            }
        ],
        "summary": {
            "total_accounts_analyzed": int,
            "suspicious_accounts_flagged": int,
            "fraud_rings_detected": int,
            "processing_time_seconds": float
        }
    }
    
    Args:
        G: Transaction graph
        transactions: Original transaction list
        cycle_accounts: Cycle detection results
        smurfing_accounts: Smurfing detection results
        shell_accounts: Shell detection results
        suspicion_scores: Account suspicion scores
        account_ring_map: Account to ring mapping
        processing_time: Processing time in seconds
        
    Returns:
        DetectionResult object matching schema
    """
    from backend.models.transaction import (
        SuspiciousAccount, FraudRing, DetectionSummary, DetectionResult
    )
    
    # Collect all unique accounts
    all_accounts = set(G.nodes())
    total_accounts = len(all_accounts)
    
    # Build account patterns map
    account_patterns: dict[str, list[str]] = defaultdict(list)
    
    # Add cycle patterns
    for ring_id, cycles in cycle_accounts.items():
        for cycle in cycles:
            pattern_label = f"cycle_length_{len(cycle)}"
            for account_id in cycle:
                if pattern_label not in account_patterns[account_id]:
                    account_patterns[account_id].append(pattern_label)
    
    # Add smurfing patterns
    for account_id, info in smurfing_accounts.items():
        pattern_label = info['pattern_label']
        if pattern_label not in account_patterns[account_id]:
            account_patterns[account_id].append(pattern_label)
    
    # Add shell patterns
    for ring_id, chains in shell_accounts.items():
        for chain in chains:
            pattern_label = f"layered_shell_{len(chain)}hop"
            for account_id in chain:
                if pattern_label not in account_patterns[account_id]:
                    account_patterns[account_id].append(pattern_label)
    
    # Build suspicious accounts list (only accounts with score > 0)
    suspicious_accounts_list = []
    for account_id in all_accounts:
        score = suspicion_scores.get(account_id, 0.0)
        if score > 0:
            patterns = account_patterns.get(account_id, [])
            ring_id = account_ring_map.get(account_id)
            
            # ensure consistent pattern order
            patterns_sorted = sorted(patterns)
            suspicious_accounts_list.append(
                SuspiciousAccount(
                    account_id=account_id,
                    suspicion_score=round(score, 1),
                    detected_patterns=patterns_sorted,
                    ring_id=ring_id
                )
            )
    
    # Sort by suspicion_score descending, then account_id ascending for determinism
    suspicious_accounts_list.sort(key=lambda x: (-x.suspicion_score, x.account_id))
    
    # Build fraud rings
    fraud_rings_list = []
    
    # Collect all unique ring IDs
    all_ring_ids = set()
    all_ring_ids.update(cycle_accounts.keys())
    all_ring_ids.update(shell_accounts.keys())
    
    # Build ring member sets
    ring_members: dict[str, set[str]] = defaultdict(set)
    
    # Add cycle ring members
    for ring_id, cycles in cycle_accounts.items():
        for cycle in cycles:
            for account_id in cycle:
                ring_members[ring_id].add(account_id)
    
    # Add shell ring members
    for ring_id, chains in shell_accounts.items():
        for chain in chains:
            for account_id in chain:
                ring_members[ring_id].add(account_id)
    
    # Create fraud ring objects
    for ring_id in all_ring_ids:
        members = sorted(list(ring_members[ring_id]))
        
        # Determine pattern type
        if ring_id in cycle_accounts:
            pattern_type = "cycle"
        elif ring_id in shell_accounts:
            pattern_type = "shell"
        else:
            pattern_type = "unknown"
        
        # Calculate risk score (average of member suspicion scores)
        member_scores = [suspicion_scores.get(m, 0.0) for m in members]
        risk_score = sum(member_scores) / len(member_scores) if member_scores else 0.0
        
        fraud_rings_list.append(
            FraudRing(
                ring_id=ring_id,
                member_accounts=members,
                pattern_type=pattern_type,
                risk_score=round(risk_score, 1)
            )
        )
    
    # Sort fraud rings by risk_score descending, then ring_id ascending
    fraud_rings_list.sort(key=lambda x: (-x.risk_score, x.ring_id))
    
    # Build summary
    summary = DetectionSummary(
        total_accounts_analyzed=total_accounts,
        suspicious_accounts_flagged=len(suspicious_accounts_list),
        fraud_rings_detected=len(fraud_rings_list),
        processing_time_seconds=round(processing_time, 2)
    )
    
    return DetectionResult(
        suspicious_accounts=suspicious_accounts_list,
        fraud_rings=fraud_rings_list,
        summary=summary
    )
