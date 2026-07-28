interface WeeklyActivityProps {
  data?: {
    day: string
    value: number
  }[]
}

function WeeklyActivity({ 
  data = [
    { day: 'Lun', value: 65 },
    { day: 'Mar', value: 80 },
    { day: 'Mié', value: 45 },
    { day: 'Jue', value: 90 },
    { day: 'Vie', value: 70 },
    { day: 'Sáb', value: 55 },
    { day: 'Dom', value: 40 }
  ]
}: WeeklyActivityProps) {
  const maxValue = Math.max(...data.map(d => d.value))

  return (
    <div className="glass-panel" style={{
      padding: '1.25rem',
      background: 'var(--glass-bg, rgba(255, 255, 255, 0.05))',
      backdropFilter: 'blur(10px)',
      border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
      borderRadius: '12px',
      marginBottom: '1.25rem'
    }}>
      <h3 style={{
        margin: '0 0 1.25rem 0',
        fontSize: '1rem',
        fontWeight: 600,
        color: 'var(--text-primary, #e2e8f0)',
        letterSpacing: '0.3px'
      }}>
        Actividad Semanal de Uso
      </h3>

      <div style={{
        display: 'flex',
        alignItems: 'flex-end',
        justifyContent: 'space-between',
        gap: '0.5rem',
        height: '120px'
      }}>
        {data.map((item, index) => (
          <div
            key={index}
            style={{
              flex: 1,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: '0.5rem'
            }}
          >
            <div
              style={{
                width: '100%',
                height: `${(item.value / maxValue) * 100}%`,
                minHeight: '20px',
                background: `linear-gradient(180deg, #7c3aed, #06b6d4)`,
                borderRadius: '8px 8px 4px 4px',
                transition: 'height 0.3s ease',
                position: 'relative',
                cursor: 'pointer'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.filter = 'brightness(1.2)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.filter = 'brightness(1)'
              }}
              title={`${item.value}% de actividad`}
            >
              <div style={{
                position: 'absolute',
                top: '-25px',
                left: '50%',
                transform: 'translateX(-50%)',
                fontSize: '0.75rem',
                fontWeight: 600,
                color: 'var(--text-primary, #e2e8f0)',
                opacity: 0,
                transition: 'opacity 0.2s'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.opacity = '1'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.opacity = '0'
              }}
            >
                {item.value}%
              </div>
            </div>
            <span style={{
              fontSize: '0.8rem',
              color: 'var(--text-secondary, #94a3b8)',
              fontWeight: 500
            }}>
              {item.day}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default WeeklyActivity
