import React from 'react'
import './DetectionSummary.css'

const DetectionSummary = ({ summary }) => {
  if (!summary) return null

  return (
    <div className="detection-summary">
      <h2>Detection Summary</h2>
      <div className="summary-grid">
        <div className="summary-card" data-icon="👥">
          <div className="summary-value">{summary.total_accounts_analyzed}</div>
          <div className="summary-label">Total Accounts Analyzed</div>
        </div>
        <div className="summary-card" data-icon="⚠️">
          <div className="summary-value highlight">
            {summary.suspicious_accounts_flagged}
          </div>
          <div className="summary-label">Suspicious Accounts Flagged</div>
        </div>
        <div className="summary-card" data-icon="🔴">
          <div className="summary-value highlight">
            {summary.fraud_rings_detected}
          </div>
          <div className="summary-label">Fraud Rings Detected</div>
        </div>
        <div className="summary-card" data-icon="⏱️">
          <div className="summary-value success">
            {summary.processing_time_seconds.toFixed(2)}s
          </div>
          <div className="summary-label">Processing Time</div>
        </div>
      </div>
    </div>
  )
}

export default DetectionSummary
