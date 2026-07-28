interface Activity {
  time: string
  icon: string
  title: string
  description: string
  xp?: number
}

interface TodayActivityProps {
  activities?: Activity[]
}

function TodayActivity({ 
  activities = [
    { time: '09:00', icon: '💬', title: 'Conversación con IA', description: 'Consulta sobre APIs en Django' },
    { time: '10:30', icon: '📚', title: 'Tutorial Terminado', description: 'HTML5 & CSS3 Moderno (+60 XP)', xp: 60 },
    { time: '11:20', icon: '🎵', title: 'Escuchaste Música', description: 'Playlist "Lo-Fi para Estudiar"' },
    { time: '13:00', icon: '🌎', title: 'Traductor Utilizado', description: 'Traducción Español ➔ In' }
  ]
}: TodayActivityProps) {
  return (
    <div className="glass-panel" style={{
      padding: '1.25rem',
      background: 'var(--glass-bg, rgba(255, 255, 255, 0.05))',
      backdropFilter: 'blur(10px)',
      border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
      borderRadius: '12px'
    }}>
      <h3 style={{
        margin: '0 0 1.25rem 0',
        fontSize: '1rem',
        fontWeight: 600,
        color: 'var(--text-primary, #e2e8f0)',
        letterSpacing: '0.3px'
      }}>
        Actividad de Hoy
      </h3>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {activities.map((activity, index) => (
          <div
            key={index}
            style={{
              display: 'flex',
              gap: '1rem',
              position: 'relative'
            }}
          >
            {/* Timeline line */}
            {index !== activities.length - 1 && (
              <div style={{
                position: 'absolute',
                left: '20px',
                top: '40px',
                bottom: '-16px',
                width: '2px',
                background: 'linear-gradient(180deg, #7c3aed, #06b6d4)',
                opacity: 0.3
              }}></div>
            )}

            {/* Time */}
            <div style={{
              minWidth: '60px',
              fontSize: '0.9rem',
              fontWeight: 600,
              color: 'var(--accent-color, #06b6d4)',
              textAlign: 'right',
              paddingTop: '4px'
            }}>
              {activity.time}
            </div>

            {/* Icon */}
            <div style={{
              width: '42px',
              height: '42px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #7c3aed, #06b6d4)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.3rem',
              flexShrink: 0,
              zIndex: 1
            }}>
              {activity.icon}
            </div>

            {/* Content */}
            <div style={{
              flex: 1,
              padding: '0.75rem 1rem',
              background: 'rgba(0, 0, 0, 0.2)',
              border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
              borderRadius: '10px',
              transition: 'all 0.2s'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'rgba(124, 58, 237, 0.1)'
              e.currentTarget.style.borderColor = 'rgba(124, 58, 237, 0.3)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'rgba(0, 0, 0, 0.2)'
              e.currentTarget.style.borderColor = 'var(--glass-border, rgba(255, 255, 255, 0.1))'
            }}
            >
              <div style={{
                fontSize: '0.95rem',
                fontWeight: 600,
                color: 'var(--text-primary, #e2e8f0)',
                marginBottom: '0.25rem',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem'
              }}>
                {activity.title}
                {activity.xp && (
                  <span style={{
                    fontSize: '0.75rem',
                    padding: '2px 8px',
                    background: 'rgba(16, 185, 129, 0.2)',
                    border: '1px solid rgba(16, 185, 129, 0.4)',
                    borderRadius: '12px',
                    color: '#10b981',
                    fontWeight: 600
                  }}>
                    +{activity.xp} XP
                  </span>
                )}
              </div>
              <div style={{
                fontSize: '0.85rem',
                color: 'var(--text-secondary, #94a3b8)'
              }}>
                {activity.description}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default TodayActivity
