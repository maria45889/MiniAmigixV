// ============================================================================
// TYPES
// ============================================================================

interface AmigisDashboardProps {
  username?: string
}

// ============================================================================
// COMPONENT
// ============================================================================

function AmigisDashboard({ username = 'mariajosetacoc2005' }: AmigisDashboardProps) {
  return (
    <div className="glass-panel" style={{
      padding: '0.5rem',
      background: 'var(--glass-bg, rgba(255, 255, 255, 0.05))',
      backdropFilter: 'blur(10px)',
      border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
      borderRadius: '10px',
      marginBottom: '0.375rem'
    }}>
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.625rem' }}>
        {/* Avatar de Amigis */}
        <div style={{
          width: '40px',
          height: '40px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #7c3aed, #06b6d4)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '1.4rem',
          flexShrink: 0,
          boxShadow: '0 4px 12px rgba(124, 58, 237, 0.3)'
        }}>
          🦆
        </div>

        {/* Contenido del mensaje */}
        <div style={{ flex: 1 }}>
          {/* Header */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.375rem',
            marginBottom: '0.375rem'
          }}>
            <h3 style={{
              margin: 0,
              fontSize: '0.85rem',
              fontWeight: 600,
              color: 'var(--text-primary, #e2e8f0)',
              letterSpacing: '0.3px'
            }}>
              ASISTENTE INTELIGENTE AMIGIS 🦆
            </h3>
          </div>

          {/* Speech Bubble */}
          <div style={{
            background: 'rgba(124, 58, 237, 0.08)',
            border: '1px solid rgba(124, 58, 237, 0.2)',
            borderRadius: '10px',
            padding: '0.5rem 0.75rem',
            position: 'relative'
          }}>
            {/* Triángulo del speech bubble */}
            <div style={{
              position: 'absolute',
              left: '-6px',
              top: '12px',
              width: 0,
              height: 0,
              borderTop: '6px solid transparent',
              borderBottom: '6px solid transparent',
              borderRight: '6px solid rgba(124, 58, 237, 0.2)'
            }}></div>

            <p style={{
              margin: 0,
              fontSize: '0.85rem',
              lineHeight: '1.5',
              color: 'var(--text-primary, #e2e8f0)'
            }}>
              "¡Bienvenida! Hoy tienes 2 eventos programados y 1 tutorial pendiente. ¿En qué trabajamos primero?"
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AmigisDashboard
