interface WeeklyGoalsProps {
  goals?: {
    id: string
    icon: string
    label: string
    current: number
    target: number
    unit: string
    completed: boolean
  }[]
}

function WeeklyGoals({ 
  goals = [
    { id: '1', icon: '📚', label: 'Estudiar 5 horas', current: 4, target: 5, unit: 'hrs', completed: false },
    { id: '2', icon: '🎵', label: 'Escuchar 10 canciones', current: 10, target: 10, unit: '', completed: true },
    { id: '3', icon: '💬', label: 'Conversar con Amigis IA', current: 1, target: 1, unit: '', completed: true }
  ]
}: WeeklyGoalsProps) {
  const completedGoals = goals.filter(g => g.completed).length
  const totalGoals = goals.length
  const percentage = Math.round((completedGoals / totalGoals) * 100)

  return (
    <div className="glass-panel" style={{
      padding: '1.25rem',
      background: 'var(--glass-bg, rgba(255, 255, 255, 0.05))',
      backdropFilter: 'blur(10px)',
      border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
      borderRadius: '12px',
      marginBottom: '1.25rem'
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '1.25rem'
      }}>
        <h3 style={{
          margin: 0,
          fontSize: '1rem',
          fontWeight: 600,
          color: 'var(--text-primary, #e2e8f0)',
          letterSpacing: '0.3px'
        }}>
          Objetivos & Meta Semanal
        </h3>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          padding: '0.5rem 1rem',
          background: 'rgba(16, 185, 129, 0.1)',
          border: '1px solid rgba(16, 185, 129, 0.3)',
          borderRadius: '20px',
          fontSize: '0.9rem',
          fontWeight: 600,
          color: '#10b981'
        }}>
          {percentage}% Completado
        </div>
      </div>

      {/* Progress bar general */}
      <div style={{
        width: '100%',
        height: '8px',
        background: 'rgba(255, 255, 255, 0.1)',
        borderRadius: '4px',
        marginBottom: '1.5rem',
        overflow: 'hidden'
      }}>
        <div style={{
          width: `${percentage}%`,
          height: '100%',
          background: 'linear-gradient(90deg, #7c3aed, #06b6d4)',
          borderRadius: '4px',
          transition: 'width 0.5s ease'
        }}></div>
      </div>

      {/* Lista de-goals */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {goals.map((goal) => (
          <div
            key={goal.id}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '1rem',
              padding: '1rem',
              background: goal.completed 
                ? 'rgba(16, 185, 129, 0.1)' 
                : 'rgba(0, 0, 0, 0.2)',
              border: goal.completed 
                ? '1px solid rgba(16, 185, 129, 0.3)' 
                : '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
              borderRadius: '10px'
            }}
          >
            <div style={{
              fontSize: '1.5rem',
              opacity: goal.completed ? 1 : 0.7
            }}>
              {goal.icon}
            </div>

            <div style={{ flex: 1 }}>
              <div style={{
                fontSize: '0.95rem',
                fontWeight: 500,
                color: 'var(--text-primary, #e2e8f0)',
                marginBottom: '0.25rem'
              }}>
                {goal.label}
              </div>
              <div style={{
                fontSize: '0.85rem',
                color: 'var(--text-secondary, #94a3b8)'
              }}>
                {goal.current} / {goal.target} {goal.unit}
              </div>
            </div>

            <div style={{
              width: '100px',
              height: '6px',
              background: 'rgba(255, 255, 255, 0.1)',
              borderRadius: '3px',
              overflow: 'hidden'
            }}>
              <div style={{
                width: `${Math.min((goal.current / goal.target) * 100, 100)}%`,
                height: '100%',
                background: goal.completed 
                  ? '#10b981' 
                  : 'linear-gradient(90deg, #7c3aed, #06b6d4)',
                borderRadius: '3px'
              }}></div>
            </div>

            {goal.completed && (
              <div style={{
                fontSize: '1.2rem',
                color: '#10b981'
              }}>
                ✔
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default WeeklyGoals
