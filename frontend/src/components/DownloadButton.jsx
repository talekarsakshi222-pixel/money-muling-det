import React from 'react'
import './DownloadButton.css'

const DownloadButton = ({ detectionResult }) => {
  const handleDownload = () => {
    if (!detectionResult) return

    const jsonString = JSON.stringify(detectionResult, null, 2)
    const blob = new Blob([jsonString], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `detection_results_${new Date().toISOString().split('T')[0]}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  return (
    <button className="download-button" onClick={handleDownload}>
      <span className="download-icon">⬇️</span>
      Download Detection Results (JSON)
    </button>
  )
}

export default DownloadButton
