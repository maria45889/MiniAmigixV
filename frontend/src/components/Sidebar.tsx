import { useState } from 'react'

interface SidebarProps {
  activeItem?: string
  onNavigate?: (item: string) => void
  onLogout?: () => void
}

function Sidebar({ activeItem = 'Inicio', onNavigate, onLogout }: SidebarProps) {
  const menuItems = [
    { section: 'Principal', items: [
      { id: 'Inicio', icon: '🏠', label: 'Inicio' },
      { id: 'Chat IA', icon: '🤖', label: 'Chat IA' },
      { id: 'Música', icon: '🎵', label: 'Música' },
      { id: 'Juegos', icon: '🎮', label: 'Juegos' },
      { id: 'Estudio', icon: '📚', label: 'Estudio' },
      { id: 'Entretenimiento', icon: '🎬', label: 'Entretenimiento' },
      { id: 'Clima', icon: '🌦️', label: 'Clima' },
      { id: 'Traductor', icon: '🌐', label: 'Traductor' },
      { id: 'Blog', icon: '📝', label: 'Blog' },
      { id: 'Eventos', icon: '📅', label: 'Eventos' },
      { id: 'Tutoriales', icon: '📖', label: 'Tutoriales' },
      { id: 'Mis Archivos', icon: '📁', label: 'Mis Archivos' },
      { id: 'Administración', icon: '⚙️', label: 'Administración' },
      { id: 'Centro Admin', icon: '🏛️', label: 'Centro Admin' },
    ]}
  ]

  return (
    <aside className="sidebar glass-panel" style={{
      width: '250px',
      display: 'flex',
      flexDirection: 'column',
      padding: '1.5rem',
      background: 'var(--glass-bg, rgba(255, 255, 255, 0.05))',
      backdropFilter: 'blur(10px)',
      border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
      borderRadius: '12px',
      height: 'calc(100vh - 2rem)',
      overflowY: 'auto'
    }}>
      {/* Logo */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '0.75rem', paddingBottom: '0.5rem', borderBottom: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))' }}>
        <img src="/favicon.svg" alt="MiniAmigixV Logo" style={{ width: '28px', height: '28px' }} />
        <h2 style={{ 
          fontSize: '1.1rem', 
          fontWeight: 'bold', 
          color: 'var(--accent-color, #06b6d4)', 
          margin: 0,
          background: 'linear-gradient(135deg, #7c3aed, #06b6d4)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text'
        }}>
          MiniAmigixV
        </h2>
      </div>
      
      {/* Menú de navegación */}
      <nav style={{ display: 'flex', flexDirection: 'column', gap: '2px', flex: 1 }}>
        {menuItems.map((section) => (
          <div key={section.section}>
            <div style={{ 
              fontSize: '0.65rem', 
              color: 'var(--text-secondary, #94a3b8)', 
              textTransform: 'uppercase', 
              letterSpacing: '1.5px', 
              marginBottom: '4px',
              marginTop: '8px',
              fontWeight: 700,
              paddingLeft: '4px'
            }}>
              {section.section}
            </div>
            {section.items.map((item) => (
              <button
                key={item.id}
                onClick={() => onNavigate?.(item.id)}
                className="glass-button"
                style={{
                  width: '100%',
                  textAlign: 'left',
                  padding: '8px 12px',
                  background: activeItem === item.id 
                    ? 'rgba(124, 58, 237, 0.15)' 
                    : 'transparent',
                  color: activeItem === item.id 
                    ? 'var(--accent-color, #06b6d4)' 
                    : 'var(--text-primary, #e2e8f0)',
                  border: activeItem === item.id 
                    ? '1px solid rgba(124, 58, 237, 0.25)' 
                    : '1px solid transparent',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  fontSize: '0.85rem',
                  marginBottom: '1px',
                  fontWeight: activeItem === item.id ? 500 : 400
                }}
                onMouseEnter={(e) => {
                  if (activeItem !== item.id) {
                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.03)'
                  }
                }}
                onMouseLeave={(e) => {
                  if (activeItem !== item.id) {
                    e.currentTarget.style.background = 'transparent'
                  }
                }}
              >
                <span style={{ fontSize: '1rem', minWidth: '20px', textAlign: 'center' }}>{item.icon}</span>
                <span>{item.label}</span>
              </button>
            ))}
          </div>
        ))}
      </nav>
      
      {/* Botón cerrar sesión */}
      <button
        onClick={onLogout}
        className="glass-button"
        style={{
          width: '100%',
          padding: '12px',
          marginTop: '1rem',
          background: 'transparent',
          color: '#ef4444',
          border: '1px solid #ef4444',
          borderRadius: '8px',
          cursor: 'pointer',
          transition: 'all 0.2s',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '8px',
          fontSize: '0.95rem',
          fontWeight: 500
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = 'rgba(239, 68, 68, 0.1)'
          e.currentTarget.style.transform = 'translateY(-2px)'
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = 'transparent'
          e.currentTarget.style.transform = 'translateY(0)'
        }}
      >
        🚪 Cerrar Sesión
      </button>
    </aside>
  )
}

export default Sidebar
