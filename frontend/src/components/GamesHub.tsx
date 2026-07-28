import { useState, useEffect } from 'react'
import TicTacToe from './TicTacToe'

interface Game {
  id: number
  nombre: string
  descripcion: string
  categoria: string
  icono: string
  activo: boolean
  fecha_creacion: string
}

interface UserStats {
  id: number
  total_puntos_xp: number
  total_monedas: number
  juegos_completados: number
  racha_dias: number
  ultima_jugada: string | null
  nivel: number
  insignia: string
}

const API_BASE = 'http://127.0.0.1:8000/api/games'

function GamesHub() {
  const [games, setGames] = useState<Game[]>([])
  const [stats, setStats] = useState<UserStats | null>(null)
  const [activeGame, setActiveGame] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'todos' | 'clasico' | 'ia' | 'educativo'>('todos')

  const token = localStorage.getItem('token')

  useEffect(() => {
    if (token) {
      fetchGames()
      fetchStats()
    } else {
      setLoading(false)
    }
  }, [token])

  const fetchGames = async () => {
    try {
      const response = await fetch(`${API_BASE}/games/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })
      if (response.ok) {
        const data = await response.json()
        setGames(data.results || data)
      }
    } catch (error) {
      console.error('Error fetching games:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_BASE}/stats/my_stats/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })
      if (response.ok) {
        const data = await response.json()
        setStats(data)
      }
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  const filteredGames = games.filter(game => {
    if (activeTab === 'todos') return true
    return game.categoria === activeTab
  })

  const renderGame = (game: Game) => {
    switch (game.nombre) {
      case 'Tres en Raya':
        return <TicTacToe onBack={() => setActiveGame(null)} />
      case 'Juego de Memoria':
        return <MemoryGame onBack={() => setActiveGame(null)} />
      case 'Snake Arcade':
        return <SnakeGame onBack={() => setActiveGame(null)} />
      default:
        return (
          <div style={{
            textAlign: 'center',
            padding: '3rem',
            color: 'var(--text-secondary, #94a3b8)'
          }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>
              {game.icono}
            </div>
            <h3>{game.nombre}</h3>
            <p>Este juego está en desarrollo...</p>
            <button
              onClick={() => setActiveGame(null)}
              style={{
                marginTop: '1rem',
                padding: '0.75rem 1.5rem',
                background: 'var(--accent-color, #8b5cf6)',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer'
              }}
            >
              Volver
            </button>
          </div>
        )
    }
  }

  if (activeGame) {
    const game = games.find(g => g.nombre === activeGame)
    return game ? renderGame(game) : null
  }

  return (
    <div style={{
      padding: '1.5rem',
      background: 'var(--glass-bg, rgba(255, 255, 255, 0.05))',
      backdropFilter: 'blur(10px)',
      border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
      borderRadius: '12px',
      color: 'var(--text-primary, #e2e8f0)',
      minHeight: '100vh'
    }}>
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '1.5rem'
      }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: 600, marginBottom: '0.5rem' }}>
            🎮 Juegos
          </h1>
          <p style={{ color: 'var(--text-secondary, #94a3b8)' }}>
            ¡Hora de divertirse! Desafía tu mente y juega junto a Amigis.
          </p>
        </div>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
          gap: '1rem',
          marginBottom: '2rem'
        }}>
          <div style={{
            padding: '1.5rem',
            background: 'var(--glass-bg, rgba(255, 255, 255, 0.08))',
            borderRadius: '12px',
            border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🎮</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 600 }}>{stats.juegos_completados}</div>
            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary, #94a3b8)' }}>
              Completados
            </div>
          </div>
          <div style={{
            padding: '1.5rem',
            background: 'var(--glass-bg, rgba(255, 255, 255, 0.08))',
            borderRadius: '12px',
            border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>⭐</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 600 }}>{stats.total_puntos_xp}</div>
            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary, #94a3b8)' }}>
              Puntos XP
            </div>
          </div>
          <div style={{
            padding: '1.5rem',
            background: 'var(--glass-bg, rgba(255, 255, 255, 0.08))',
            borderRadius: '12px',
            border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🪙</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 600 }}>{stats.total_monedas}</div>
            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary, #94a3b8)' }}>
              Monedas Amigis
            </div>
          </div>
          <div style={{
            padding: '1.5rem',
            background: 'var(--glass-bg, rgba(255, 255, 255, 0.08))',
            borderRadius: '12px',
            border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🔥</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 600 }}>{stats.racha_dias} días</div>
            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary, #94a3b8)' }}>
              Racha Diaria
            </div>
          </div>
          <div style={{
            padding: '1.5rem',
            background: 'var(--glass-bg, rgba(255, 255, 255, 0.08))',
            borderRadius: '12px',
            border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🏅</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 600 }}>Nivel {stats.nivel}</div>
            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary, #94a3b8)' }}>
              {stats.insignia}
            </div>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div style={{
        display: 'flex',
        gap: '0.5rem',
        marginBottom: '1.5rem',
        borderBottom: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
        paddingBottom: '0.5rem'
      }}>
        <button
          onClick={() => setActiveTab('todos')}
          style={{
            padding: '0.75rem 1.5rem',
            background: activeTab === 'todos' ? 'var(--accent-color, #8b5cf6)' : 'transparent',
            color: 'var(--text-primary, #e2e8f0)',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '1rem'
          }}
        >
          Todos
        </button>
        <button
          onClick={() => setActiveTab('clasico')}
          style={{
            padding: '0.75rem 1.5rem',
            background: activeTab === 'clasico' ? 'var(--accent-color, #8b5cf6)' : 'transparent',
            color: 'var(--text-primary, #e2e8f0)',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '1rem'
          }}
        >
          Clásicos
        </button>
        <button
          onClick={() => setActiveTab('ia')}
          style={{
            padding: '0.75rem 1.5rem',
            background: activeTab === 'ia' ? 'var(--accent-color, #8b5cf6)' : 'transparent',
            color: 'var(--text-primary, #e2e8f0)',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '1rem'
          }}
        >
          Juegos con IA
        </button>
        <button
          onClick={() => setActiveTab('educativo')}
          style={{
            padding: '0.75rem 1.5rem',
            background: activeTab === 'educativo' ? 'var(--accent-color, #8b5cf6)' : 'transparent',
            color: 'var(--text-primary, #e2e8f0)',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '1rem'
          }}
        >
          Educativos
        </button>
      </div>

      {/* Games Grid */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          Cargando juegos...
        </div>
      ) : (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
          gap: '1.5rem'
        }}>
          {filteredGames.map((game) => (
            <div
              key={game.id}
              style={{
                padding: '1.5rem',
                background: 'var(--glass-bg, rgba(255, 255, 255, 0.05))',
                borderRadius: '12px',
                border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
              onClick={() => setActiveGame(game.nombre)}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'var(--glass-bg, rgba(255, 255, 255, 0.1))'
                e.currentTarget.style.transform = 'translateY(-4px)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'var(--glass-bg, rgba(255, 255, 255, 0.05))'
                e.currentTarget.style.transform = 'translateY(0)'
              }}
            >
              <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>
                {game.icono}
              </div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.5rem' }}>
                {game.nombre}
              </h3>
              <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary, #94a3b8)', marginBottom: '1rem' }}>
                {game.descripcion}
              </p>
              <button
                style={{
                  padding: '0.75rem 1.5rem',
                  background: 'var(--accent-color, #8b5cf6)',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontSize: '1rem',
                  fontWeight: 500,
                  width: '100%'
                }}
              >
                Jugar Ahora
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

// Memory Game
function MemoryGame({ onBack }: { onBack: () => void }) {
  const [cards, setCards] = useState<string[]>([])
  const [flipped, setFlipped] = useState<number[]>([])
  const [matched, setMatched] = useState<number[]>([])
  const [moves, setMoves] = useState(0)

  const emojis = ['🎮', '🎲', '🎯', '🎪', '🎨', '🎭', '🎪', '🎨', '🎭', '🎮', '🎲', '🎯']

  useEffect(() => {
    shuffleCards()
  }, [])

  const shuffleCards = () => {
    const shuffled = [...emojis].sort(() => Math.random() - 0.5)
    setCards(shuffled)
    setFlipped([])
    setMatched([])
    setMoves(0)
  }

  const handleCardClick = (index: number) => {
    if (flipped.length === 2 || flipped.includes(index) || matched.includes(index)) return

    const newFlipped = [...flipped, index]
    setFlipped(newFlipped)

    if (newFlipped.length === 2) {
      setMoves(moves + 1)
      const [first, second] = newFlipped
      if (cards[first] === cards[second]) {
        setMatched([...matched, first, second])
        setFlipped([])
      } else {
        setTimeout(() => setFlipped([]), 1000)
      }
    }
  }

  return (
    <div style={{ padding: '1.5rem' }}>
      <button
        onClick={onBack}
        style={{
          marginBottom: '1rem',
          padding: '0.5rem 1rem',
          background: 'transparent',
          color: 'var(--text-primary, #e2e8f0)',
          border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
          borderRadius: '8px',
          cursor: 'pointer'
        }}
      >
        ← Volver
      </button>
      <h2 style={{ marginBottom: '1rem' }}>🧠 Juego de Memoria</h2>
      <p style={{ marginBottom: '1rem', color: 'var(--text-secondary, #94a3b8)' }}>
        Encuentra los pares de cartas idénticas en el menor tiempo posible.
      </p>
      <div style={{ marginBottom: '1rem' }}>
        Movimientos: {moves}
      </div>
      {matched.length === cards.length && (
        <div style={{
          marginBottom: '1rem',
          padding: '1rem',
          background: 'rgba(34, 197, 94, 0.2)',
          borderRadius: '8px',
          textAlign: 'center',
          fontWeight: 600
        }}>
          ¡Completado en {moves} movimientos!
        </div>
      )}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(4, 1fr)',
        gap: '0.5rem',
        maxWidth: '400px',
        margin: '0 auto 1.5rem'
      }}>
        {cards.map((card, index) => (
          <button
            key={index}
            onClick={() => handleCardClick(index)}
            disabled={matched.includes(index)}
            style={{
              aspectRatio: '1',
              fontSize: '2rem',
              background: flipped.includes(index) || matched.includes(index)
                ? 'var(--glass-bg, rgba(255, 255, 255, 0.15))'
                : 'var(--accent-color, #8b5cf6)',
              border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
              borderRadius: '8px',
              cursor: matched.includes(index) ? 'default' : 'pointer',
              opacity: matched.includes(index) ? 0.5 : 1
            }}
          >
            {flipped.includes(index) || matched.includes(index) ? card : '?'}
          </button>
        ))}
      </div>
      <button
        onClick={shuffleCards}
        style={{
          padding: '0.75rem 1.5rem',
          background: 'var(--accent-color, #8b5cf6)',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          cursor: 'pointer'
        }}
      >
        Reiniciar
      </button>
    </div>
  )
}

// Snake Game
function SnakeGame({ onBack }: { onBack: () => void }) {
  const [snake, setSnake] = useState([[5, 5]])
  const [food, setFood] = useState([10, 10])
  const [direction, setDirection] = useState('RIGHT')
  const [gameOver, setGameOver] = useState(false)
  const [score, setScore] = useState(0)

  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      switch (e.key) {
        case 'ArrowUp':
          if (direction !== 'DOWN') setDirection('UP')
          break
        case 'ArrowDown':
          if (direction !== 'UP') setDirection('DOWN')
          break
        case 'ArrowLeft':
          if (direction !== 'RIGHT') setDirection('LEFT')
          break
        case 'ArrowRight':
          if (direction !== 'LEFT') setDirection('RIGHT')
          break
      }
    }
    window.addEventListener('keydown', handleKeyPress)
    return () => window.removeEventListener('keydown', handleKeyPress)
  }, [direction])

  useEffect(() => {
    if (gameOver) return
    const interval = setInterval(() => {
      moveSnake()
    }, 150)
    return () => clearInterval(interval)
  }, [snake, direction, food, gameOver])

  const moveSnake = () => {
    const newSnake = [...snake]
    const head = { ...newSnake[0] }

    switch (direction) {
      case 'UP':
        head[1] -= 1
        break
      case 'DOWN':
        head[1] += 1
        break
      case 'LEFT':
        head[0] -= 1
        break
      case 'RIGHT':
        head[0] += 1
        break
    }

    // Check collision with walls
    if (head[0] < 0 || head[0] >= 20 || head[1] < 0 || head[1] >= 20) {
      setGameOver(true)
      return
    }

    // Check collision with self
    if (newSnake.some(segment => segment[0] === head[0] && segment[1] === head[1])) {
      setGameOver(true)
      return
    }

    newSnake.unshift([head[0], head[1]])

    // Check if ate food
    if (head[0] === food[0] && head[1] === food[1]) {
      setScore(score + 1)
      setFood([
        Math.floor(Math.random() * 20),
        Math.floor(Math.random() * 20)
      ])
    } else {
      newSnake.pop()
    }

    setSnake(newSnake)
  }

  const resetGame = () => {
    setSnake([[5, 5]])
    setFood([10, 10])
    setDirection('RIGHT')
    setGameOver(false)
    setScore(0)
  }

  return (
    <div style={{ padding: '1.5rem' }}>
      <button
        onClick={onBack}
        style={{
          marginBottom: '1rem',
          padding: '0.5rem 1rem',
          background: 'transparent',
          color: 'var(--text-primary, #e2e8f0)',
          border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
          borderRadius: '8px',
          cursor: 'pointer'
        }}
      >
        ← Volver
      </button>
      <h2 style={{ marginBottom: '1rem' }}>🐍 Snake Arcade</h2>
      <p style={{ marginBottom: '1rem', color: 'var(--text-secondary, #94a3b8)' }}>
        Guía a la serpiente para comer las manzanas sin chocar con los bordes.
      </p>
      <div style={{ marginBottom: '1rem' }}>
        Puntuación: {score}
      </div>
      {gameOver && (
        <div style={{
          marginBottom: '1rem',
          padding: '1rem',
          background: 'rgba(239, 68, 68, 0.2)',
          borderRadius: '8px',
          textAlign: 'center',
          fontWeight: 600
        }}>
          ¡Game Over! Puntuación: {score}
        </div>
      )}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(20, 1fr)',
          gap: '1px',
          maxWidth: '400px',
          margin: '0 auto 1.5rem',
          background: 'var(--glass-border, rgba(255, 255, 255, 0.1))',
          padding: '1px',
          borderRadius: '8px'
        }}
      >
        {Array.from({ length: 20 }).map((_, y) =>
          Array.from({ length: 20 }).map((_, x) => {
            const isSnake = snake.some(segment => segment[0] === x && segment[1] === y)
            const isFood = food[0] === x && food[1] === y
            return (
              <div
                key={`${x}-${y}`}
                style={{
                  aspectRatio: '1',
                  background: isSnake
                    ? '#22c55e'
                    : isFood
                    ? '#ef4444'
                    : 'var(--bg-dark, #0f172a)',
                  borderRadius: '2px'
                }}
              />
            )
          })
        )}
      </div>
      <button
        onClick={resetGame}
        style={{
          padding: '0.75rem 1.5rem',
          background: 'var(--accent-color, #8b5cf6)',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          cursor: 'pointer'
        }}
      >
        Reiniciar
      </button>
      <p style={{ marginTop: '1rem', fontSize: '0.875rem', color: 'var(--text-secondary, #94a3b8)' }}>
        Usa las flechas del teclado para mover la serpiente
      </p>
    </div>
  )
}

export default GamesHub
