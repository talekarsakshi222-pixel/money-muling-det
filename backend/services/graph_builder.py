"""Graph construction from transactions."""
import networkx as nx
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.transaction import Transaction


def build_transaction_graph(transactions: list['Transaction']) -> nx.DiGraph:
    """
    Build directed graph from transactions.
    
    Nodes: account IDs (sender_id, receiver_id)
    Edges: transactions with attributes (amount, timestamp, transaction_id)
    
    Complexity: O(n) where n = number of transactions
    
    Args:
        transactions: List of Transaction objects
        
    Returns:
        Directed graph with edge attributes
    """
    G = nx.DiGraph()
    
    for tx in transactions:
        # Add edge with transaction data as attributes
        if G.has_edge(tx.sender_id, tx.receiver_id):
            # If edge exists, append to list (multiple transactions between same accounts)
            if 'transactions' not in G[tx.sender_id][tx.receiver_id]:
                # Convert existing single transaction to list
                existing = G[tx.sender_id][tx.receiver_id]
                G[tx.sender_id][tx.receiver_id]['transactions'] = [existing]
                G[tx.sender_id][tx.receiver_id]['amount'] = existing.get('amount', 0)
                G[tx.sender_id][tx.receiver_id]['timestamp'] = existing.get('timestamp')
            
            G[tx.sender_id][tx.receiver_id]['transactions'].append({
                'transaction_id': tx.transaction_id,
                'amount': tx.amount,
                'timestamp': tx.timestamp
            })
            G[tx.sender_id][tx.receiver_id]['amount'] += tx.amount
        else:
            # New edge
            G.add_edge(
                tx.sender_id,
                tx.receiver_id,
                amount=tx.amount,
                timestamp=tx.timestamp,
                transaction_id=tx.transaction_id,
                transactions=[{
                    'transaction_id': tx.transaction_id,
                    'amount': tx.amount,
                    'timestamp': tx.timestamp
                }]
            )
    
    return G
