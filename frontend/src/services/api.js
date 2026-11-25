// This file handles communication with the FastAPI backend.
// Keeping API calls in a separate file makes the UI code cleaner.

const API_BASE_URL = 'http://127.0.0.1:8001'

export async function predictStudent(studentData) {
  // fetch sends an HTTP request to the backend.
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(studentData),
  })

  // If the backend returns an error status, throw an error with detail.
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || 'Prediction request failed')
  }

  return response.json()
}
