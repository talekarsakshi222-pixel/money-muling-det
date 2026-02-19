import React, { useState } from 'react'
import CSVUpload from './components/CSVUpload'
import GraphVisualization from './components/GraphVisualization'
import FraudRingTable from './components/FraudRingTable'
import DetectionSummary from './components/DetectionSummary'
import DownloadButton from './components/DownloadButton'
import './App.css'

function App() {
  const [detectionResult, setDetectionResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleDetectionComplete = (result) => {
    setDetectionResult(result)
    setError(null)
  }

  const handleError = (err) => {
    setError(err)
    setDetectionResult(null)
  }

  const handleLoading = (isLoading) => {
    setLoading(isLoading)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Money Muling Detection Engine</h1>
        <p>Graph-Based Financial Crime Detection System</p>
      </header>

      <main className="app-main">
        <div className="upload-section">
          <CSVUpload
            onDetectionComplete={handleDetectionComplete}
            onError={handleError}
            onLoading={handleLoading}
          />
        </div>

        {error && (
          <div className="error-message">
            <h3>Error</h3>
            <p>{error}</p>
          </div>
        )}

        {loading && (
          <div className="loading-message">
            <p>Processing transactions... This may take a moment.</p>
          </div>
        )}

        {detectionResult && (
          <>
            <DetectionSummary summary={detectionResult.summary} />
            
            <div className="results-section">
              <div className="graph-section">
                <h2>Transaction Graph Visualization</h2>
                <GraphVisualization
                  detectionResult={detectionResult}
                />
              </div>

              <div className="table-section">
                <h2>Fraud Rings Detected</h2>
                <FraudRingTable fraudRings={detectionResult.fraud_rings} />
              </div>
            </div>

            <div className="download-section">
              <DownloadButton detectionResult={detectionResult} />
            </div>
          </>
        )}
      </main>

      <footer className="app-footer">
        <p>Money Muling Detection Engine v1.0.0</p>
      </footer>
    </div>
  )
}

export default App
