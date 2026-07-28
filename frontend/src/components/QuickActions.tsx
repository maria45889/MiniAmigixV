interface QuickActionsProps {
  onAction?: (action: string) => void
}

function QuickActions({ onAction }: QuickActionsProps) {
  const actions = [
    { id: 'chat', icon: '💬', label: 'Nuevo Chat', color: '#7c3aed' },
    { id: 'course', icon: '📚', label: 'Continuar Curso', color: '#06b6d4' },
    { id: 'music', icon: '🎵', label: 'Reproducir Música', color: '#ec4899' },
    { id: 'translate', icon: '🌎', label: 'Traducir', color: '#10b981' },
    { id: 'event', icon: '📅', label: 'Crear Evento', color: '#f59e0b' },
    { id: 'files', icon: '📁', label: 'Abrir Archivos', color: '#3b82f6' },
  ]

  return (
    <div className="glass-panel" style={{
      padding: '0.5rem',
      background: 'var(--glass-bg, rgba(255, 255, 255, 0.05))',
      backdropFilter: 'blur(10px)',
      border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
      borderRadius: '10px',
      marginBottom: '0.5rem'
    }}>
      <h3 style={{
        margin: '0 0 0.375rem 0',
        fontSize: '0.85rem',
        fontWeight: 600,
        color: 'var(--text-primary, #e2e8f0)',
        letterSpacing: '0.3px'
      }}>
        Acciones Rápidas
      </h3>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(110px, 1fr))',
        gap: '0.375rem'
      }}>
        {actions.map((action) => (
          <button
            key={action.id}
            onClick={() => onAction?.(action.id)}
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: '0.375rem',
              padding: '0.625rem',
              background: 'rgba(0, 0, 0, 0.15)',
              border: `1px solid ${action.color}30`,
              borderRadius: '10px',
              cursor: 'pointer',
              transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
              color: 'var(--text-primary, #e2e8f0)',
              position: 'relative',
              overflow: 'hidden'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = `${action.color}15`
              e.currentTarget.style.transform = 'translateY(-2px) scale(1.02)'
              e.currentTarget.style.boxShadow = `0 6px 16px ${action.color}25`
              e.currentTarget.style.borderColor = action.color
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'rgba(0, 0, 0, 0.15)'
              e.currentTarget.style.transform = 'translateY(0) scale(1)'
              e.currentTarget.style.boxShadow = 'none'
              e.currentTarget.style.borderColor = `${action.color}30`
            }}
          >
            <span style={{ 
              fontSize: '1.4rem',
              filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.2))'
            }}>
              {action.icon}
            </span>
            <span style={{ 
              fontSize: '0.75rem', 
              fontWeight: 600,
              letterSpacing: '0.2px'
            }}>
              {action.label}
            </span>
          </button>
        ))}
      </div>
    </div>
  )
}

export default QuickActions
