import { useState } from 'react'
import ThemeToggle from './ThemeToggle'
import { useTheme } from '../contexts/ThemeContext'

interface HeaderProps {
  username?: string
  onLogout?: () => void
}

function Header({ username = 'mariajosetacoc2005', onLogout }: HeaderProps) {
  const [searchQuery, setSearchQuery] = useState('')
  const [showProfileMenu, setShowProfileMenu] = useState(false)

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('Buscando:', searchQuery)
  }

  return (
    <header className="header glass-panel" style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0.75rem 1.5rem',
      background: 'var(--glass-bg, rgba(255, 255, 255, 0.05))',
      backdropFilter: 'blur(10px)',
      border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
      borderRadius: '12px',
      marginBottom: '1rem'
    }}>
      {/* Logo y breadcrumb */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <img src="/favicon.svg" alt="MiniAmigixV Logo" style={{ width: '28px', height: '28px' }} />
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-secondary, #94a3b8)', fontSize: '0.85rem' }}>
          <span style={{ fontWeight: 500 }}>MiniAmigixV</span>
          <span style={{ opacity: 0.5 }}>/</span>
          <span style={{ color: 'var(--text-primary, #e2e8f0)', fontWeight: 500 }}>Inicio</span>
        </div>
      </div>

      {/* Barra de búsqueda */}
      <form onSubmit={handleSearch} style={{ flex: 1, maxWidth: '350px', margin: '0 1.5rem' }}>
        <div style={{ position: 'relative' }}>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Buscar..."
            style={{
              width: '100%',
              padding: '8px 14px 8px 36px',
              background: 'rgba(0, 0, 0, 0.2)',
              border: '1px solid var(--glass-border, #2d3748)',
              borderRadius: '8px',
              color: 'var(--text-primary, #f1f5f9)',
              fontSize: '0.85rem',
              outline: 'none',
              transition: 'border-color 0.2s, box-shadow 0.2s'
            }}
            onFocus={(e) => {
              e.target.style.borderColor = '#06b6d4'
              e.target.style.boxShadow = '0 0 0 2px rgba(6, 182, 212, 0.2)'
            }}
            onBlur={(e) => {
              e.target.style.borderColor = 'var(--glass-border, #2d3748)'
              e.target.style.boxShadow = 'none'
            }}
          />
          <span style={{ 
            position: 'absolute', 
            left: '10px', 
            top: '50%', 
            transform: 'translateY(-50%)',
            color: 'var(--text-secondary, #94a3b8)',
            fontSize: '0.9rem'
          }}>
            🔍
          </span>
        </div>
      </form>

      {/* Perfil de usuario */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        {/* Theme Toggle */}
        <ThemeToggle />

        {/* Notificaciones */}
        <button style={{
          background: 'none',
          border: 'none',
          fontSize: '1.1rem',
          cursor: 'pointer',
          padding: '6px',
          borderRadius: '8px',
          transition: 'background 0.2s'
        }}
        onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.1)'}
        onMouseLeave={(e) => e.currentTarget.style.background = 'none'}
        >
          🔔
        </button>

        {/* Avatar y menú */}
        <div style={{ position: 'relative' }}>
          <button
            onClick={() => setShowProfileMenu(!showProfileMenu)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              background: 'rgba(124, 58, 237, 0.15)',
              border: '1px solid rgba(124, 58, 237, 0.25)',
              borderRadius: '8px',
              padding: '5px 10px',
              cursor: 'pointer',
              transition: 'transform 0.2s, box-shadow 0.2s'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-1px)'
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(124, 58, 237, 0.25)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)'
              e.currentTarget.style.boxShadow = 'none'
            }}
          >
            <div style={{
              width: '28px',
              height: '28px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #7c3aed, #06b6d4)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 'bold',
              fontSize: '0.85rem',
              color: 'white'
            }}>
              {username.charAt(0).toUpperCase()}
            </div>
            <span style={{ color: 'var(--text-primary, #e2e8f0)', fontSize: '0.85rem', fontWeight: 500 }}>
              {username}
            </span>
          </button>

          {/* Menú desplegable */}
          {showProfileMenu && (
            <div style={{
              position: 'absolute',
              top: '100%',
              right: 0,
              marginTop: '8px',
              background: 'var(--glass-bg, rgba(30, 41, 59, 0.95))',
              backdropFilter: 'blur(10px)',
              border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
              borderRadius: '12px',
              padding: '8px 0',
              minWidth: '200px',
              zIndex: 1000,
              boxShadow: '0 4px 20px rgba(0, 0, 0, 0.3)'
            }}>
              <div style={{ padding: '12px 16px', borderBottom: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1)' }}>
                <p style={{ margin: 0, fontSize: '0.85rem', color: 'var(--text-secondary, #94a3b8)' }}>
                  Ha iniciado sesión exitosamente como
                </p>
                <p style={{ margin: '4px 0 0 0', fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary, #e2e8f0)' }}>
                  {username}
                </p>
              </div>
              <button style={{
                width: '100%',
                padding: '10px 16px',
                background: 'none',
                border: 'none',
                color: 'var(--text-primary, #e2e8f0)',
                textAlign: 'left',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                fontSize: '0.9rem',
                transition: 'background 0.2s'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)'}
              onMouseLeave={(e) => e.currentTarget.style.background = 'none'}
              >
                📊 Dashboard General
              </button>
              <button style={{
                width: '100%',
                padding: '10px 16px',
                background: 'none',
                border: 'none',
                color: 'var(--text-primary, #e2e8f0)',
                textAlign: 'left',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                fontSize: '0.9rem',
                transition: 'background 0.2s'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)'}
              onMouseLeave={(e) => e.currentTarget.style.background = 'none'}
              >
                👤 Perfil
              </button>
              <button style={{
                width: '100%',
                padding: '10px 16px',
                background: 'none',
                border: 'none',
                color: 'var(--text-primary, #e2e8f0)',
                textAlign: 'left',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                fontSize: '0.9rem',
                transition: 'background 0.2s'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)'}
              onMouseLeave={(e) => e.currentTarget.style.background = 'none'}
              >
                ⚙️ Ajustes
              </button>
              <div style={{ height: '1px', background: 'var(--glass-border, rgba(255, 255, 255, 0.1)', margin: '8px 0' }}></div>
              <button
                onClick={onLogout}
                style={{
                  width: '100%',
                  padding: '10px 16px',
                  background: 'none',
                  border: 'none',
                  color: '#ef4444',
                  textAlign: 'left',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  fontSize: '0.9rem',
                  transition: 'background 0.2s'
                }}
                onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(239, 68, 68, 0.1)'}
                onMouseLeave={(e) => e.currentTarget.style.background = 'none'}
              >
                🚪 Cerrar Sesión
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}

export default Header
