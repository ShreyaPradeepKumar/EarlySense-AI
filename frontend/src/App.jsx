import { useState } from 'react'
import { predictStudent } from './services/api'
import StudentForm from './components/StudentForm'
import PredictionResult from './components/PredictionResult'

/*
  App.jsx is the main component.
  It stores state (form data, loading, error, result) and coordinates
  the form and result components.
*/
function App() {
  const [formData, setFormData] = useState({
    gender: 'female',
    'race/ethnicity': 'group B',
    'parental level of education': "bachelor's degree",
    lunch: 'standard',
    'test preparation course': 'none',
  })

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)

  // Update form state when user changes an input.
  function handleChange(event) {
    const { name, value } = event.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  // Submit form: call backend API and show prediction.
  async function handleSubmit(event) {
    event.preventDefault()
    setLoading(true)
    setError('')
    setResult(null)

    try {
      const prediction = await predictStudent(formData)
      setResult(prediction)
    } catch (err) {
      setError(err.message || 'Something went wrong while predicting.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>EarlySense AI</h1>
        <p>Simple student risk prediction using Machine Learning</p>
      </header>

      <main className="main-content">
        <StudentForm
          formData={formData}
          onChange={handleChange}
          onSubmit={handleSubmit}
          loading={loading}
        />
        <PredictionResult result={result} error={error} loading={loading} />
      </main>

      <footer className="footer">
      </footer>
    </div>
  )
}

export default App
