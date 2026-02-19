import React, { useEffect, useRef } from 'react'
import cytoscape from 'cytoscape'
import dagre from 'cytoscape-dagre'
import './GraphVisualization.css'

// Register dagre layout
cytoscape.use(dagre)

const GraphVisualization = ({ detectionResult, transactions }) => {
  const containerRef = useRef(null)
  const cyRef = useRef(null)

  useEffect(() => {
    if (!detectionResult || !containerRef.current) return

    // Build sets for quick lookup
    const suspiciousAccountIds = new Set(
      detectionResult.suspicious_accounts.map(acc => acc.account_id)
    )
    
    const accountScores = {}
    detectionResult.suspicious_accounts.forEach(acc => {
      accountScores[acc.account_id] = acc.suspicion_score
    })

    // Get all unique accounts from transactions if available
    let allAccountIds = new Set()
    if (transactions && transactions.length > 0) {
      transactions.forEach(tx => {
        allAccountIds.add(tx.sender_id)
        allAccountIds.add(tx.receiver_id)
      })
    } else {
      // Fallback to all accounts from detection result
      allAccountIds = new Set([
        ...detectionResult.suspicious_accounts.map(acc => acc.account_id),
        ...detectionResult.fraud_rings.flatMap(ring => ring.member_accounts)
      ])
    }

    // Create nodes for ALL accounts
    const nodes = Array.from(allAccountIds).map(accountId => {
      const score = accountScores[accountId] || 0
      const suspiciousAcc = detectionResult.suspicious_accounts.find(
        acc => acc.account_id === accountId
      )
      
      let classes = 'normal'
      if (score > 50) {
        classes = 'suspicious-high'
      } else if (score > 0) {
        classes = 'suspicious-medium'
      }
      
      return {
        data: {
          id: accountId,
          label: accountId,
          suspicion_score: score,
          patterns: suspiciousAcc?.detected_patterns?.join(', ') || '',
          ring_id: suspiciousAcc?.ring_id || '',
        },
        classes: classes,
      }
    })

    // Create edges - ALL transaction edges plus ring connections
    const edges = []
    const edgeSet = new Set()
    
    // Add transaction edges if available
    if (transactions && transactions.length > 0) {
      transactions.forEach((tx, idx) => {
        const edgeId = `tx-${tx.sender_id}-${tx.receiver_id}-${idx}`
        if (!edgeSet.has(edgeId)) {
          edgeSet.add(edgeId)
          edges.push({
            data: {
              id: edgeId,
              source: tx.sender_id,
              target: tx.receiver_id,
              edge_type: 'transaction',
            },
            classes: 'transaction-edge',
          })
        }
      })
    }
    
    // Add ring connection edges (between ring members)
    detectionResult.fraud_rings.forEach(ring => {
      for (let i = 0; i < ring.member_accounts.length; i++) {
        for (let j = i + 1; j < ring.member_accounts.length; j++) {
          const source = ring.member_accounts[i]
          const target = ring.member_accounts[j]
          
          const edgeId = `ring-${source}-${target}-${ring.ring_id}`
          if (!edgeSet.has(edgeId)) {
            edgeSet.add(edgeId)
            edges.push({
              data: {
                id: edgeId,
                source: source,
                target: target,
                ring_id: ring.ring_id,
                edge_type: 'ring',
              },
              classes: 'ring-edge',
            })
          }
        }
      }
    })

    // Initialize Cytoscape
    if (cyRef.current) {
      cyRef.current.destroy()
    }

    cyRef.current = cytoscape({
      container: containerRef.current,
      elements: [...nodes, ...edges],
      style: [
        {
          selector: 'node',
          style: {
            'background-color': '#667eea',
            'label': 'data(label)',
            'width': 40,
            'height': 40,
            'font-size': '10px',
            'text-valign': 'center',
            'text-halign': 'center',
            'color': '#333',
            'border-width': 2,
            'border-color': '#fff',
          },
        },
        {
          selector: 'node.suspicious-high',
          style: {
            'background-color': '#e53e3e',
            'width': 60,
            'height': 60,
            'font-size': '12px',
            'font-weight': 'bold',
          },
        },
        {
          selector: 'node.suspicious-medium',
          style: {
            'background-color': '#f6ad55',
            'width': 50,
            'height': 50,
            'font-size': '11px',
          },
        },
        {
          selector: 'edge',
          style: {
            'width': 2,
            'line-color': '#999',
            'target-arrow-color': '#999',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'opacity': 0.6,
          },
        },
      ],
      layout: {
        name: 'dagre',
        rankDir: 'LR',
        spacingFactor: 1.5,
      },
    })

    // Add hover tooltips using title attribute
    cyRef.current.on('mouseover', 'node', function (evt) {
      const node = evt.target
      const data = node.data()
      const tooltipText = `Account: ${data.label}\nScore: ${data.suspicion_score.toFixed(1)}\nPatterns: ${data.patterns || 'None'}${data.ring_id ? `\nRing: ${data.ring_id}` : ''}`
      node.style('label', `${data.label}\n(${data.suspicion_score.toFixed(1)})`)
    })

    cyRef.current.on('mouseout', 'node', function (evt) {
      const node = evt.target
      const data = node.data()
      node.style('label', data.label)
    })

    // Cleanup
    return () => {
      if (cyRef.current) {
        cyRef.current.destroy()
        cyRef.current = null
      }
    }
  }, [detectionResult])

  return (
    <div className="graph-visualization">
      <div className="graph-legend">
        <div className="legend-item">
          <div className="legend-color high"></div>
          <span>High Suspicion (Score &gt; 50)</span>
        </div>
        <div className="legend-item">
          <div className="legend-color medium"></div>
          <span>Medium Suspicion (Score ≤ 50)</span>
        </div>
      </div>
      <div ref={containerRef} className="cytoscape-container"></div>
    </div>
  )
}

export default GraphVisualization
