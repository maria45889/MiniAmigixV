import { useState, useEffect } from 'react'
import './index.css'
import AmigisMascot from './components/AmigisMascot'

function App() {
  const [apiStatus, setApiStatus] = useState<string>('Verificando conexión...')
  const [isLight, setIsLight] = useState(false)

  useEffect(() => {
    // Basic API connection check
    fetch('http://127.0.0.1:8000/api/')
      .then(res => {
        if (res.ok || res.status === 404) return 'Conectado a Django Backend'
        throw new Error('Network response was not ok.')
      })
      .then(msg => setApiStatus(msg))
      .catch(() => setApiStatus('Error conectando al backend'))

    // Theme logic
    const prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches
    setIsLight(prefersLight)
    document.documentElement.setAttribute('data-theme', prefersLight ? 'light' : 'dark')

    const handleThemeChange = (e: MediaQueryListEvent) => {
      setIsLight(e.matches)
      document.documentElement.setAttribute('data-theme', e.matches ? 'light' : 'dark')
    }

    const mediaQuery = window.matchMedia('(prefers-color-scheme: light)')
    mediaQuery.addEventListener('change', handleThemeChange)

    return () => mediaQuery.removeEventListener('change', handleThemeChange)
  }, [])

  const toggleTheme = () => {
    setIsLight(!isLight)
    document.documentElement.setAttribute('data-theme', !isLight ? 'light' : 'dark')
  }

  // Placeholder handlers for Mascot
  const handleAIResponse = () => console.log('Amigis: IA respondiendo')
  const handleMusicPlay = () => console.log('Amigis: Música activada')
  const handleWeatherLoad = () => console.log('Amigis: Clima actualizado')
  const handleGameStart = () => console.log('Amigis: Juego iniciado')
  const handleTranslation = () => console.log('Amigis: Traducción completada')

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar glass-panel">
        <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--accent-color)', marginBottom: '2rem' }}>
          MiniAmigixV
        </h2>
        
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <button className="glass-button" style={{ textAlign: 'left', background: 'transparent', color: 'var(--text-primary)', border: '1px solid var(--glass-border)' }}>🏠 Inicio</button>
          <button className="glass-button" style={{ textAlign: 'left', background: 'transparent', color: 'var(--text-primary)', border: '1px solid var(--glass-border)' }}>🤖 Chat IA</button>
          <button className="glass-button" style={{ textAlign: 'left', background: 'transparent', color: 'var(--text-primary)', border: '1px solid var(--glass-border)' }}>🌦️ Clima</button>
          <button className="glass-button" style={{ textAlign: 'left', background: 'transparent', color: 'var(--text-primary)', border: '1px solid var(--glass-border)' }}>📝 Blog</button>
          <button className="glass-button" style={{ textAlign: 'left', background: 'transparent', color: 'var(--text-primary)', border: '1px solid var(--glass-border)' }}>👤 Perfil</button>
        </nav>

        <div style={{ marginTop: 'auto', padding: '16px', borderRadius: '12px', background: 'var(--glass-bg)', border: '1px solid var(--glass-border)', fontSize: '0.8rem' }}>
          <p>API Status:</p>
          <p style={{ color: apiStatus.includes('Error') ? '#ef4444' : '#10b981', fontWeight: 600 }}>{apiStatus}</p>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="header glass-panel">
          <div>
            <h1 style={{ fontSize: '1.8rem' }}>Bienvenido de nuevo 👋</h1>
            <p style={{ color: 'var(--text-secondary)' }}>Aquí tienes un resumen de tu actividad de hoy.</p>
          </div>
          
          <button className="glass-button" onClick={toggleTheme} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            {isLight ? '🌙 Modo Oscuro' : '☀️ Modo Claro'}
          </button>
        </header>

        <div className="dashboard-grid">
          <div className="card glass-panel">
            <h3>🤖 Últimas Conversaciones</h3>
            <p>Conéctate con tus asistentes virtuales favoritos y retoma donde lo dejaste.</p>
            <button className="glass-button" style={{ marginTop: 'auto' }}>Abrir Chat IA</button>
          </div>
          
          <div className="card glass-panel">
            <h3>🌦️ Clima Local</h3>
            <p>Actualmente soleado. La temperatura perfecta para seguir programando.</p>
            <button className="glass-button" style={{ marginTop: 'auto' }}>Ver Pronóstico</button>
          </div>

          <div className="card glass-panel">
            <h3>📝 Novedades en el Blog</h3>
            <p>Lee los últimos artículos de tecnología e inteligencia artificial publicados hoy.</p>
            <button className="glass-button" style={{ marginTop: 'auto' }}>Leer Blog</button>
          </div>
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
      </main>
    </div>
  )
}

export default App
