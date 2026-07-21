import { useState, useEffect } from 'react'
import './App.css'
import AmigisMascot from './components/AmigisMascot'

function App() {
  const [message, setMessage] = useState<string>('Cargando...')
  const [isLight, setIsLight] = useState(false)

  useEffect(() => {
    // Test connection to Django backend
    fetch('http://127.0.0.1:8000/')
      .then(res => res.text())
      .then(data => setMessage('Conectado a Django Backend'))
      .catch(err => setMessage('Error conectando al backend'))

    // Detect theme preference
    const prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches
    setIsLight(prefersLight)

    const handleThemeChange = (e: MediaQueryListEvent) => {
      setIsLight(e.matches)
    }

    const mediaQuery = window.matchMedia('(prefers-color-scheme: light)')
    mediaQuery.addEventListener('change', handleThemeChange)

    return () => {
      mediaQuery.removeEventListener('change', handleThemeChange)
    }
  }, [])

  const toggleTheme = () => {
    setIsLight(!isLight)
    document.body.classList.toggle('light')
  }

  const handleAIResponse = () => {
    console.log('Amigis: IA respondiendo')
  }

  const handleMusicPlay = () => {
    console.log('Amigis: Música activada')
  }

  const handleWeatherLoad = () => {
    console.log('Amigis: Clima actualizado')
  }

  const handleGameStart = () => {
    console.log('Amigis: Juego iniciado')
  }

  const handleTranslation = () => {
    console.log('Amigis: Traducción completada')
  }

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif', minHeight: '100vh', backgroundColor: isLight ? '#f5f5f5' : '#1a1a2e', color: isLight ? '#333' : '#eee' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>MiniAmigixV - Frontend React</h1>
        <button 
          onClick={toggleTheme}
          style={{
            padding: '0.5rem 1rem',
            borderRadius: '8px',
            border: 'none',
            cursor: 'pointer',
            backgroundColor: isLight ? '#7C3AED' : '#FFD700',
            color: isLight ? 'white' : '#333',
            fontSize: '1rem'
          }}
        >
          {isLight ? '🌙 Modo Oscuro' : '☀️ Modo Claro'}
        </button>
      </div>
      
      <p>Status: {message}</p>
      <p>Backend URL: http://127.0.0.1:8000</p>
      <p>Frontend URL: http://localhost:5173</p>
      
      <div style={{ marginTop: '2rem', padding: '1rem', backgroundColor: isLight ? '#fff' : '#2d2d44', borderRadius: '8px' }}>
        <h2>🦆 Amigis - La Mascota Patito Programador</h2>
        <p>¡Hola! Soy Amigis, tu asistente de código. Haz clic en mí para interactuar.</p>
        <ul style={{ marginTop: '1rem' }}>
          <li>✨ Animaciones suaves y expresivas</li>
          <li>💻 Laptop que aparece cuando la IA responde</li>
          <li>🌙☀️ Cambio de color según el tema</li>
          <li>👀 Ojos que siguen el cursor</li>
          <li>🎉 Reacciona a eventos de la aplicación</li>
        </ul>
      </div>

      {/* Amigis Mascot */}
      <AmigisMascot
        onThemeChange={(light) => setIsLight(light)}
        onAIResponse={handleAIResponse}
        onMusicPlay={handleMusicPlay}
        onWeatherLoad={handleWeatherLoad}
        onGameStart={handleGameStart}
        onTranslation={handleTranslation}
      />
    </div>
  )
}

export default App
