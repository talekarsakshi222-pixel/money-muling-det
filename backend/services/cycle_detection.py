"""Cycle detection algorithm for money muling rings."""
import networkx as nx
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from networkx import DiGraph


def detect_cycles(G: 'DiGraph', min_length: int = 3, max_length: int = 5) -> dict[str, list[list[str]]]:
    """
    Detect simple cycles of specified length range.
    
    Algorithm: Uses NetworkX simple_cycles with bounded length.
    Complexity: O((n+m) * c) where:
        - n = nodes, m = edges
        - c = number of cycles (can be exponential in worst case, but bounded by max_length)
    
    Args:
        G: Directed graph
        min_length: Minimum cycle length (default: 3)
        max_length: Maximum cycle length (default: 5)
        
    Returns:
        Dictionary mapping ring_id to list of cycles (each cycle is list of node IDs)
    """
    cycles = []
    
    # Get all simple cycles
    # Note: simple_cycles can be expensive for large graphs, but max_length=5 bounds it
    # nx.simple_cycles may return cycles in graph-dependent order; sort for determinism
    all_cycles = list(nx.simple_cycles(G))
    # sort cycles by tuple for consistency
    all_cycles.sort(key=lambda c: tuple(c))
    
    # Filter by length
    filtered_cycles = [
        cycle for cycle in all_cycles
        if min_length <= len(cycle) <= max_length
    ]
    
    if not filtered_cycles:
        return {}
    
    # Group cycles by shared nodes (same ring)
    ring_map: dict[str, list[list[str]]] = {}
    ring_counter = 1
    node_to_ring: dict[str, str] = {}
    
    for cycle in filtered_cycles:
        # Check if any node in cycle already belongs to a ring
        existing_ring = None
        for node in cycle:
            if node in node_to_ring:
                existing_ring = node_to_ring[node]
                break
        
        if existing_ring:
            ring_id = existing_ring
        else:
            ring_id = f"RING_{ring_counter:03d}"
            ring_counter += 1
        
        # Add cycle to ring
        if ring_id not in ring_map:
            ring_map[ring_id] = []
        ring_map[ring_id].append(cycle)
        
        # Mark all nodes in cycle as belonging to this ring
        for node in cycle:
            node_to_ring[node] = ring_id
    
    return ring_map


def get_cycle_pattern_label(cycle_length: int) -> str:
    """Generate pattern label for cycle detection."""
    return f"cycle_length_{cycle_length}"
