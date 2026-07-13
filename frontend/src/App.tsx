import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState<string>('Cargando...')

  useEffect(() => {
    // Test connection to Django backend
    fetch('http://127.0.0.1:8000/')
      .then(res => res.text())
      .then(data => setMessage('Conectado a Django Backend'))
      .catch(err => setMessage('Error conectando al backend'))
  }, [])

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif' }}>
      <h1>MiniAmigixV - Frontend React</h1>
      <p>Status: {message}</p>
      <p>Backend URL: http://127.0.0.1:8000</p>
      <p>Frontend URL: http://localhost:5173</p>
    </div>
  )
}

export default App
