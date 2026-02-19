"""Layered shell detection: chains with low-degree intermediate nodes."""
from typing import TYPE_CHECKING, Set

if TYPE_CHECKING:
    from networkx import DiGraph


def detect_layered_shells(G: 'DiGraph', min_chain_length: int = 3, max_intermediate_degree: int = 3) -> dict[str, list[list[str]]]:
    """
    Detect layered shell patterns: chains with low-degree intermediate nodes.
    
    Pattern: Chain of length >= min_chain_length where intermediate nodes
    have total degree <= max_intermediate_degree.
    
    Algorithm: DFS-based chain detection with degree filtering.
    Complexity: O(n * d^l) where:
        - n = nodes
        - d = average degree
        - l = chain length (bounded by graph structure)
    
    Args:
        G: Directed graph
        min_chain_length: Minimum chain length (default: 3)
        max_intermediate_degree: Maximum degree for intermediate nodes (default: 3)
        
    Returns:
        Dictionary mapping ring_id to list of chains (each chain is list of node IDs)
    """
    chains = []
    
    # Find all nodes that could be chain starts (high out-degree potential)
    # and chain ends (high in-degree potential)
    # use sorted node lists for deterministic behavior
    potential_starts = [n for n in sorted(G.nodes()) if G.out_degree(n) > 0]
    potential_ends = [n for n in sorted(G.nodes()) if G.in_degree(n) > 0]
    
    # DFS to find chains
    visited_chains: set[tuple] = set()
    
    def is_valid_intermediate(node: str, position: int, chain_length: int) -> bool:
        """Check if node can be intermediate node in chain."""
        if position == 0 or position == chain_length - 1:
            return True  # Start/end nodes have no restrictions
        total_degree = G.in_degree(node) + G.out_degree(node)
        return total_degree <= max_intermediate_degree
    
    def dfs_chain(current: str, chain: list[str], target_length: int):
        """DFS to find chains of target length."""
        if len(chain) == target_length:
            chain_tuple = tuple(sorted(chain))
            if chain_tuple not in visited_chains:
                # Validate intermediate nodes
                valid = all(
                    is_valid_intermediate(chain[i], i, target_length)
                    for i in range(1, target_length - 1)
                )
                if valid:
                    chains.append(chain.copy())
                    visited_chains.add(chain_tuple)
            return
        
        # Continue chain
        for neighbor in G.successors(current):
            if neighbor not in chain:  # Avoid cycles
                chain.append(neighbor)
                dfs_chain(neighbor, chain, target_length)
                chain.pop()
    
    # Try different chain lengths
    for length in range(min_chain_length, min_chain_length + 3):  # Try lengths 3, 4, 5
        for start in potential_starts:
            dfs_chain(start, [start], length)
    
    if not chains:
        return {}
    
    # Group chains by shared nodes (same ring)
    ring_map: dict[str, list[list[str]]] = {}
    ring_counter = 1
    node_to_ring: dict[str, str] = {}
    
    for chain in chains:
        # Check if any node in chain already belongs to a ring
        existing_ring = None
        for node in chain:
            if node in node_to_ring:
                existing_ring = node_to_ring[node]
                break
        
        if existing_ring:
            ring_id = existing_ring
        else:
            ring_id = f"RING_{ring_counter:03d}"
            ring_counter += 1
        
        # Add chain to ring
        if ring_id not in ring_map:
            ring_map[ring_id] = []
        ring_map[ring_id].append(chain)
        
        # Mark all nodes in chain as belonging to this ring
        for node in chain:
            node_to_ring[node] = ring_id
    
    return ring_map


def get_shell_pattern_label(chain_length: int) -> str:
    """Generate pattern label for shell detection."""
    return f"layered_shell_{chain_length}hop"
