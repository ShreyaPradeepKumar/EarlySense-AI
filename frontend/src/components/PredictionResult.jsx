/*
  PredictionResult component shows loading, error, or prediction output.
*/
function PredictionResult({ result, error, loading }) {
  return (
    <section className="card">
      <h2>Prediction Result</h2>
      <p className="card-subtitle">The model output will appear here.</p>

      {loading && <p className="info">Running prediction...</p>}

      {error && <div className="error-box">{error}</div>}

      {!loading && !error && !result && (
        <p className="info">Submit the form to see the prediction.</p>
      )}
      {result && (
        <div className={`result-box ${result.at_risk ? 'risk' : 'safe'}`}>
          <h3>{result.risk_label}</h3>
          <p><strong>Probability of Risk:</strong> {(result.probability * 100).toFixed(2)}%</p>
          <p>{result.message}</p>
          <p className="note">
            Note: This prediction is based on available background features and a model trained on
            historical student performance data. It is an early warning, not a final judgment.
          </p>
        </div>
      )}
    </section>
  )
}

export default PredictionResult
