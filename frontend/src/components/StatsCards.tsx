interface StatsCardsProps {
  stats?: {
    chats: number
    courses: number
    musicHours: number
    games: number
    translations: number
    files: number
    streak: number
    level: number
  }
}

function StatsCards({ 
  stats = {
    chats: 124,
    courses: 12,
    musicHours: 36,
    games: 45,
    translations: 89,
    files: 14,
    streak: 18,
    level: 35
  }
}: StatsCardsProps) {
  const cards = [
    { icon: '💬', label: 'Chats IA', value: stats.chats, color: '#7c3aed' },
    { icon: '📚', label: 'Cursos', value: stats.courses, color: '#06b6d4' },
    { icon: '🎵', label: 'Música', value: `${stats.musicHours}h`, color: '#ec4899' },
    { icon: '🎮', label: 'Juegos', value: stats.games, color: '#f59e0b' },
    { icon: '🌎', label: 'Traducciones', value: stats.translations, color: '#10b981' },
    { icon: '📁', label: 'Archivos', value: stats.files, color: '#3b82f6' },
    { icon: '🔥', label: 'Días Racha', value: stats.streak, color: '#ef4444' },
    { icon: '⭐', label: 'Nivel Actual', value: `Nv. ${stats.level}`, color: '#8b5cf6' },
  ]

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(100px, 1fr))',
      gap: '0.375rem',
      marginBottom: '0.5rem'
    }}>
      {cards.map((card, index) => (
        <div
          key={index}
          className="glass-panel"
          style={{
            padding: '0.625rem',
            background: 'var(--glass-bg, rgba(255, 255, 255, 0.05))',
            backdropFilter: 'blur(10px)',
            border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
            borderRadius: '10px',
            textAlign: 'center',
            transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
            cursor: 'pointer',
            position: 'relative',
            overflow: 'hidden'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-3px) scale(1.03)'
            e.currentTarget.style.boxShadow = `0 8px 16px ${card.color}25`
            e.currentTarget.style.borderColor = card.color
            e.currentTarget.style.background = `${card.color}10`
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0) scale(1)'
            e.currentTarget.style.boxShadow = 'none'
            e.currentTarget.style.borderColor = 'var(--glass-border, rgba(255, 255, 255, 0.1))'
            e.currentTarget.style.background = 'var(--glass-bg, rgba(255, 255, 255, 0.05))'
          }}
        >
          <div style={{ 
            fontSize: '1.5rem', 
            marginBottom: '0.25rem',
            filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.2))'
          }}>
            {card.icon}
          </div>
          <div style={{
            fontSize: '1.15rem',
            fontWeight: 700,
            color: card.color,
            marginBottom: '0.125rem',
            textShadow: `0 0 20px ${card.color}40`
          }}>
            {card.value}
          </div>
          <div style={{
            fontSize: '0.7rem',
            color: 'var(--text-secondary, #94a3b8)',
            fontWeight: 500,
            letterSpacing: '0.2px'
          }}>
            {card.label}
          </div>
        </div>
      ))}
    </div>
  )
}

export default StatsCards
