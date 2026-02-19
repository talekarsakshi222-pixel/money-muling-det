import React from 'react'
import './FraudRingTable.css'

const FraudRingTable = ({ fraudRings }) => {
  if (!fraudRings || fraudRings.length === 0) {
    return (
      <div className="no-rings">
        <p>No fraud rings detected.</p>
      </div>
    )
  }

  return (
    <div className="fraud-ring-table-container">
      <table className="fraud-ring-table">
        <thead>
          <tr>
            <th>Ring ID</th>
            <th>Pattern Type</th>
            <th>Member Count</th>
            <th>Risk Score</th>
            <th>Member Accounts</th>
          </tr>
        </thead>
        <tbody>
          {fraudRings.map((ring) => (
            <tr key={ring.ring_id}>
              <td className="ring-id">{ring.ring_id}</td>
              <td>
                <span className={`pattern-badge pattern-${ring.pattern_type}`}>
                  {ring.pattern_type}
                </span>
              </td>
              <td>{ring.member_accounts.length}</td>
              <td>
                <span className={`risk-score risk-${getRiskLevel(ring.risk_score)}`}>
                  {ring.risk_score.toFixed(1)}
                </span>
              </td>
              <td className="member-accounts">
                {ring.member_accounts.join(', ')}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

const getRiskLevel = (score) => {
  if (score >= 70) return 'high'
  if (score >= 40) return 'medium'
  return 'low'
}

export default FraudRingTable
