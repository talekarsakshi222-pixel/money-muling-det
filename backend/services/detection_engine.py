"""Main detection engine orchestrating all detection algorithms."""
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from networkx import DiGraph
    from backend.models.transaction import Transaction, DetectionResult

from backend.services.graph_builder import build_transaction_graph
from backend.services.cycle_detection import detect_cycles
from backend.services.smurfing_detection import detect_smurfing
from backend.services.shell_detection import detect_layered_shells
from backend.services.scoring import calculate_suspicion_scores
from backend.services.json_formatter import format_detection_result


def run_detection(transactions: list['Transaction']) -> 'DetectionResult':
    """
    Run complete detection pipeline.
    
    Steps:
    1. Build transaction graph
    2. Detect cycles
    3. Detect smurfing patterns
    4. Detect layered shells
    5. Calculate suspicion scores
    6. Format results
    
    Args:
        transactions: List of Transaction objects
        
    Returns:
        DetectionResult matching output schema
    """
    start_time = time.time()
    
    # Step 1: Build graph
    G = build_transaction_graph(transactions)
    
    # Step 2: Detect cycles
    cycle_accounts = detect_cycles(G, min_length=3, max_length=5)
    
    # Step 3: Detect smurfing
    smurfing_accounts = detect_smurfing(G, transactions, threshold=10, time_window_hours=72)
    
    # Step 4: Detect shells
    shell_accounts = detect_layered_shells(G, min_chain_length=3, max_intermediate_degree=3)
    
    # filter shell chains that intersect with cycle accounts (cycles take priority)
    if shell_accounts:
        cycle_accounts_set = {
            acct
            for cycles in cycle_accounts.values()
            for cycle in cycles
            for acct in cycle
        }
        filtered_shell: dict[str, list[list[str]]] = {}
        for ring_id, chains in shell_accounts.items():
            remaining = [chain for chain in chains if all(acct not in cycle_accounts_set for acct in chain)]
            if remaining:
                filtered_shell[ring_id] = remaining
        shell_accounts = filtered_shell
    
    # Step 5: Build account-to-ring mapping
    account_ring_map: dict[str, str] = {}
    
    # Assign cycle accounts first (cycles have priority)
    for ring_id, cycles in cycle_accounts.items():
        for cycle in cycles:
            for account_id in cycle:
                account_ring_map[account_id] = ring_id
    
    # Rename remaining shell ring IDs to avoid collisions with cycle IDs and assign mappings
    if shell_accounts:
        new_shell_accounts: dict[str, list[list[str]]] = {}
        start_index = len(cycle_accounts) + 1
        for idx, (old_id, chains) in enumerate(shell_accounts.items(), start=start_index):
            new_id = f"RING_{idx:03d}"
            new_shell_accounts[new_id] = chains
            # map accounts if not already assigned
            for chain in chains:
                for account_id in chain:
                    if account_id not in account_ring_map:
                        account_ring_map[account_id] = new_id
        shell_accounts = new_shell_accounts
    
    # Step 6: Calculate suspicion scores
    suspicion_scores = calculate_suspicion_scores(
        G, transactions, cycle_accounts, smurfing_accounts,
        shell_accounts, account_ring_map
    )
    
    # Step 7: Format results
    processing_time = time.time() - start_time
    
    result = format_detection_result(
        G, transactions, cycle_accounts, smurfing_accounts,
        shell_accounts, suspicion_scores, account_ring_map, processing_time
    )
    
    return result
