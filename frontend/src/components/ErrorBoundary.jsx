import React from 'react'

// ErrorBoundary catches rendering errors so the app shows a message instead of a blank screen.
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: 24, fontFamily: 'Arial, sans-serif' }}>
          <h2>Something went wrong</h2>
          <p style={{ color: '#b91c1c' }}>{String(this.state.error)}</p>
          <button onClick={() => window.location.reload()}>Reload</button>
        </div>
      )
    }
    return this.props.children
  }
}

export default ErrorBoundary
