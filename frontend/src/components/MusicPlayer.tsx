import { useState, useEffect } from 'react'

interface Song {
  id: number
  titulo: string
  artista: string
  album?: string
  duracion?: number
  youtube_url?: string
  youtube_video_id?: string
  portada_url?: string
  letra?: string
  fecha_agregada: string
}

interface Playlist {
  id: number
  nombre: string
  descripcion?: string
  canciones: any[]
  total_canciones: number
  es_publica: boolean
}

interface MusicSettings {
  id: number
  volumen: number
  repetir: string
  aleatorio: boolean
  ultima_cancion?: Song
}

const API_BASE = 'http://127.0.0.1:8000/api/music'

function MusicPlayer() {
  const [songs, setSongs] = useState<Song[]>([])
  const [playlists, setPlaylists] = useState<Playlist[]>([])
  const [favorites, setFavorites] = useState<Song[]>([])
  const [currentSong, setCurrentSong] = useState<Song | null>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [volume, setVolume] = useState(0.7)
  const [isShuffle, setIsShuffle] = useState(false)
  const [repeatMode, setRepeatMode] = useState<'none' | 'one' | 'all'>('none')
  const [currentTime, setCurrentTime] = useState(0)
  const [showAddSong, setShowAddSong] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState<'library' | 'playlists' | 'favorites'>('library')
  const [showVideo, setShowVideo] = useState(false)

  // Form for adding song
  const [newSong, setNewSong] = useState({
    titulo: '',
    artista: '',
    album: '',
    youtube_url: '',
  })

  const token = localStorage.getItem('token')

  // Fetch data
  useEffect(() => {
    if (token) {
      fetchSongs()
      fetchPlaylists()
      fetchFavorites()
      fetchSettings()
    } else {
      setLoading(false)
    }
  }, [token])

  const fetchSongs = async () => {
    try {
      const response = await fetch(`${API_BASE}/songs/library/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })
      if (response.ok) {
        const data = await response.json()
        setSongs(data)
      }
    } catch (error) {
      console.error('Error fetching songs:', error)
    }
  }

  const fetchPlaylists = async () => {
    try {
      const response = await fetch(`${API_BASE}/playlists/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })
      if (response.ok) {
        const data = await response.json()
        setPlaylists(data.results || data)
      }
    } catch (error) {
      console.error('Error fetching playlists:', error)
    }
  }

  const fetchFavorites = async () => {
    try {
      const response = await fetch(`${API_BASE}/favorites/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })
      if (response.ok) {
        const data = await response.json()
        setFavorites(data.results || data)
      }
    } catch (error) {
      console.error('Error fetching favorites:', error)
    }
  }

  const fetchSettings = async () => {
    try {
      const response = await fetch(`${API_BASE}/settings/my_settings/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })
      if (response.ok) {
        const data: MusicSettings = await response.json()
        setVolume(data.volumen)
        setIsShuffle(data.aleatorio)
        setRepeatMode(data.repetir as 'none' | 'one' | 'all')
        if (data.ultima_cancion) {
          setCurrentSong(data.ultima_cancion)
        }
      }
    } catch (error) {
      console.error('Error fetching settings:', error)
    }
  }

  const handleAddSong = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE}/songs/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newSong),
      })
      if (response.ok) {
        await fetchSongs()
        setNewSong({ titulo: '', artista: '', album: '', youtube_url: '' })
        setShowAddSong(false)
      }
    } catch (error) {
      console.error('Error adding song:', error)
    } finally {
      setLoading(false)
    }
  }

  const handlePlaySong = async (song: Song) => {
    setCurrentSong(song)
    setIsPlaying(true)
    try {
      await fetch(`${API_BASE}/songs/${song.id}/play/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ posicion: 0 }),
      })
    } catch (error) {
      console.error('Error playing song:', error)
    }
  }

  const handleToggleFavorite = async (songId: number) => {
    try {
      const response = await fetch(`${API_BASE}/favorites/toggle/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ cancion_id: songId }),
      })
      if (response.ok) {
        const data = await response.json()
        if (data.is_favorite) {
          await fetchFavorites()
        } else {
          setFavorites(prev => prev.filter(s => s.id !== songId))
        }
      }
    } catch (error) {
      console.error('Error toggling favorite:', error)
    }
  }

  const handleUpdateVolume = async (newVolume: number) => {
    setVolume(newVolume)
    try {
      await fetch(`${API_BASE}/settings/update_volume/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ volumen: newVolume }),
      })
    } catch (error) {
      console.error('Error updating volume:', error)
    }
  }

  const handleToggleShuffle = async () => {
    const newShuffle = !isShuffle
    setIsShuffle(newShuffle)
    try {
      await fetch(`${API_BASE}/settings/toggle_shuffle/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })
    } catch (error) {
      console.error('Error toggling shuffle:', error)
    }
  }

  const handleSetRepeat = async (mode: 'none' | 'one' | 'all') => {
    setRepeatMode(mode)
    try {
      await fetch(`${API_BASE}/settings/set_repeat/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ repeat_mode: mode }),
      })
    } catch (error) {
      console.error('Error setting repeat:', error)
    }
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const filteredSongs = songs.filter(song =>
    song.titulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    song.artista.toLowerCase().includes(searchTerm.toLowerCase())
  )

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
            🎵 Música
          </h1>
          <p style={{ color: 'var(--text-secondary, #94a3b8)' }}>
            Disfruta de tu música favorita y la mejor compañía sonora.
          </p>
        </div>
        <button
          onClick={() => setShowAddSong(!showAddSong)}
          style={{
            padding: '0.75rem 1.5rem',
            background: 'var(--accent-color, #8b5cf6)',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '1rem',
            fontWeight: 500
          }}
        >
          {showAddSong ? 'Cancelar' : '+ Añadir Canción'}
        </button>
      </div>

      {/* Add Song Form */}
      {showAddSong && (
        <div style={{
          background: 'var(--glass-bg, rgba(255, 255, 255, 0.08))',
          padding: '1.5rem',
          borderRadius: '12px',
          marginBottom: '1.5rem',
          border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))'
        }}>
          <h3 style={{ marginBottom: '1rem' }}>Añadir Nueva Canción</h3>
          <form onSubmit={handleAddSong} style={{ display: 'grid', gap: '1rem' }}>
            <input
              type="text"
              placeholder="Nombre de la canción"
              value={newSong.titulo}
              onChange={(e) => setNewSong({ ...newSong, titulo: e.target.value })}
              required
              style={{
                padding: '0.75rem',
                background: 'var(--bg-dark, #0f172a)',
                border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
                borderRadius: '8px',
                color: 'var(--text-primary, #e2e8f0)'
              }}
            />
            <input
              type="text"
              placeholder="Artista"
              value={newSong.artista}
              onChange={(e) => setNewSong({ ...newSong, artista: e.target.value })}
              required
              style={{
                padding: '0.75rem',
                background: 'var(--bg-dark, #0f172a)',
                border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
                borderRadius: '8px',
                color: 'var(--text-primary, #e2e8f0)'
              }}
            />
            <input
              type="text"
              placeholder="Álbum (opcional)"
              value={newSong.album}
              onChange={(e) => setNewSong({ ...newSong, album: e.target.value })}
              style={{
                padding: '0.75rem',
                background: 'var(--bg-dark, #0f172a)',
                border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
                borderRadius: '8px',
                color: 'var(--text-primary, #e2e8f0)'
              }}
            />
            <input
              type="url"
              placeholder="YouTube URL (opcional)"
              value={newSong.youtube_url}
              onChange={(e) => setNewSong({ ...newSong, youtube_url: e.target.value })}
              style={{
                padding: '0.75rem',
                background: 'var(--bg-dark, #0f172a)',
                border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
                borderRadius: '8px',
                color: 'var(--text-primary, #e2e8f0)'
              }}
            />
            <button
              type="submit"
              disabled={loading}
              style={{
                padding: '0.75rem 1.5rem',
                background: 'var(--accent-color, #8b5cf6)',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: loading ? 'not-allowed' : 'pointer',
                fontSize: '1rem',
                fontWeight: 500,
                opacity: loading ? 0.6 : 1
              }}
            >
              {loading ? 'Añadiendo...' : 'Añadir a la Biblioteca'}
            </button>
          </form>
        </div>
      )}

      {/* YouTube Video Player */}
      {currentSong && currentSong.youtube_video_id && (
        <div style={{
          background: 'var(--glass-bg, rgba(255, 255, 255, 0.08))',
          padding: '1.5rem',
          borderRadius: '12px',
          marginBottom: '1.5rem',
          border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ margin: 0 }}>🎬 Video en Vivo</h3>
            <button
              onClick={() => setShowVideo(!showVideo)}
              style={{
                padding: '0.5rem 1rem',
                background: 'var(--accent-color, #8b5cf6)',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer'
              }}
            >
              {showVideo ? 'Ocultar Video' : 'Mostrar Video'}
            </button>
          </div>
          {showVideo ? (
            <div style={{
              position: 'relative',
              paddingBottom: '56.25%',
              height: 0,
              overflow: 'hidden',
              borderRadius: '8px'
            }}>
              <iframe
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                  border: 0
                }}
                src={`https://www.youtube.com/embed/${currentSong.youtube_video_id}?autoplay=${isPlaying ? 1 : 0}`}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                title={currentSong.titulo}
              />
            </div>
          ) : (
            <div style={{
              textAlign: 'center',
              padding: '2rem',
              color: 'var(--text-secondary, #94a3b8)'
            }}>
              🎬 Selecciona una canción de YouTube para ver el video aquí
            </div>
          )}
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
          onClick={() => setActiveTab('library')}
          style={{
            padding: '0.75rem 1.5rem',
            background: activeTab === 'library' ? 'var(--accent-color, #8b5cf6)' : 'transparent',
            color: 'var(--text-primary, #e2e8f0)',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '1rem'
          }}
        >
          📚 Biblioteca
        </button>
        <button
          onClick={() => setActiveTab('playlists')}
          style={{
            padding: '0.75rem 1.5rem',
            background: activeTab === 'playlists' ? 'var(--accent-color, #8b5cf6)' : 'transparent',
            color: 'var(--text-primary, #e2e8f0)',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '1rem'
          }}
        >
          🎧 Playlists
        </button>
        <button
          onClick={() => setActiveTab('favorites')}
          style={{
            padding: '0.75rem 1.5rem',
            background: activeTab === 'favorites' ? 'var(--accent-color, #8b5cf6)' : 'transparent',
            color: 'var(--text-primary, #e2e8f0)',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '1rem'
          }}
        >
          ❤️ Favoritos
        </button>
      </div>

      {/* Search */}
      <div style={{ marginBottom: '1.5rem' }}>
        <input
          type="text"
          placeholder="Buscar en biblioteca..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            width: '100%',
            padding: '0.75rem 1rem',
            background: 'var(--bg-dark, #0f172a)',
            border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
            borderRadius: '8px',
            color: 'var(--text-primary, #e2e8f0)',
            fontSize: '1rem'
          }}
        />
      </div>

      {/* Content */}
      {activeTab === 'library' && (
        <div>
          <h3 style={{ marginBottom: '1rem' }}>Tu Biblioteca</h3>
          {filteredSongs.length === 0 ? (
            <div style={{
              textAlign: 'center',
              padding: '3rem',
              color: 'var(--text-secondary, #94a3b8)'
            }}>
              📭 Tu biblioteca está vacía.
              <br />
              Agrega una canción desde el panel de arriba.
            </div>
          ) : (
            <div style={{ display: 'grid', gap: '0.75rem' }}>
              {filteredSongs.map((song) => (
                <div
                  key={song.id}
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '1rem',
                    background: 'var(--glass-bg, rgba(255, 255, 255, 0.05))',
                    borderRadius: '8px',
                    border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
                    cursor: 'pointer',
                    transition: 'all 0.2s'
                  }}
                  onClick={() => handlePlaySong(song)}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = 'var(--glass-bg, rgba(255, 255, 255, 0.1))'
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = 'var(--glass-bg, rgba(255, 255, 255, 0.05))'
                  }}
                >
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 600, marginBottom: '0.25rem' }}>
                      {song.titulo}
                    </div>
                    <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary, #94a3b8)' }}>
                      {song.artista}
                      {song.album && ` • ${song.album}`}
                    </div>
                  </div>
                  <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handleToggleFavorite(song.id)
                      }}
                      style={{
                        padding: '0.5rem',
                        background: 'transparent',
                        border: 'none',
                        cursor: 'pointer',
                        fontSize: '1.25rem'
                      }}
                    >
                      {favorites.some(f => f.id === song.id) ? '❤️' : '🤍'}
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handlePlaySong(song)
                      }}
                      style={{
                        padding: '0.5rem 1rem',
                        background: 'var(--accent-color, #8b5cf6)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '6px',
                        cursor: 'pointer'
                      }}
                    >
                      ▶️
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'playlists' && (
        <div>
          <h3 style={{ marginBottom: '1rem' }}>Playlists</h3>
          {playlists.length === 0 ? (
            <div style={{
              textAlign: 'center',
              padding: '3rem',
              color: 'var(--text-secondary, #94a3b8)'
            }}>
              No tienes playlists aún.
              <br />
              Crea una para organizar tu música.
            </div>
          ) : (
            <div style={{ display: 'grid', gap: '0.75rem' }}>
              {playlists.map((playlist) => (
                <div
                  key={playlist.id}
                  style={{
                    padding: '1.5rem',
                    background: 'var(--glass-bg, rgba(255, 255, 255, 0.05))',
                    borderRadius: '12px',
                    border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))'
                  }}
                >
                  <div style={{ fontWeight: 600, fontSize: '1.125rem', marginBottom: '0.5rem' }}>
                    {playlist.nombre}
                  </div>
                  <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary, #94a3b8)' }}>
                    {playlist.descripcion || 'Sin descripción'}
                  </div>
                  <div style={{ marginTop: '0.5rem', fontSize: '0.875rem' }}>
                    {playlist.total_canciones} canciones
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'favorites' && (
        <div>
          <h3 style={{ marginBottom: '1rem' }}>Mis Favoritos</h3>
          {favorites.length === 0 ? (
            <div style={{
              textAlign: 'center',
              padding: '3rem',
              color: 'var(--text-secondary, #94a3b8)'
            }}>
              No tienes canciones favoritas aún.
              <br />
              Añade algunas desde tu biblioteca.
            </div>
          ) : (
            <div style={{ display: 'grid', gap: '0.75rem' }}>
              {favorites.map((song) => (
                <div
                  key={song.id}
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '1rem',
                    background: 'var(--glass-bg, rgba(255, 255, 255, 0.05))',
                    borderRadius: '8px',
                    border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
                    cursor: 'pointer'
                  }}
                  onClick={() => handlePlaySong(song)}
                >
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 600, marginBottom: '0.25rem' }}>
                      {song.titulo}
                    </div>
                    <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary, #94a3b8)' }}>
                      {song.artista}
                    </div>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      handlePlaySong(song)
                    }}
                    style={{
                      padding: '0.5rem 1rem',
                      background: 'var(--accent-color, #8b5cf6)',
                      color: 'white',
                      border: 'none',
                      borderRadius: '6px',
                      cursor: 'pointer'
                    }}
                  >
                    ▶️
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Now Playing Bar */}
      {currentSong && (
        <div style={{
          position: 'fixed',
          bottom: '0',
          left: '0',
          right: '0',
          padding: '1rem 2rem',
          background: 'var(--bg-dark, #0f172a)',
          borderTop: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
          display: 'flex',
          alignItems: 'center',
          gap: '1.5rem',
          zIndex: 1000
        }}>
          {/* Song Info */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flex: 1 }}>
            <div style={{
              width: '48px',
              height: '48px',
              background: 'var(--accent-color, #8b5cf6)',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.5rem'
            }}>
              🎵
            </div>
            <div>
              <div style={{ fontWeight: 600 }}>{currentSong.titulo}</div>
              <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary, #94a3b8)' }}>
                {currentSong.artista}
              </div>
            </div>
          </div>

          {/* Controls */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <button
              onClick={handleToggleShuffle}
              style={{
                padding: '0.5rem',
                background: 'transparent',
                border: 'none',
                cursor: 'pointer',
                fontSize: '1.25rem',
                opacity: isShuffle ? 1 : 0.5
              }}
            >
              🔀
            </button>
            <button
              style={{
                padding: '0.5rem',
                background: 'transparent',
                border: 'none',
                cursor: 'pointer',
                fontSize: '1.25rem'
              }}
            >
              ⏮
            </button>
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              style={{
                padding: '0.75rem',
                background: 'var(--accent-color, #8b5cf6)',
                color: 'white',
                border: 'none',
                borderRadius: '50%',
                cursor: 'pointer',
                fontSize: '1.5rem',
                width: '48px',
                height: '48px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              {isPlaying ? '⏸' : '▶️'}
            </button>
            <button
              style={{
                padding: '0.5rem',
                background: 'transparent',
                border: 'none',
                cursor: 'pointer',
                fontSize: '1.25rem'
              }}
            >
              ⏭
            </button>
            <button
              onClick={() => {
                const modes: ('none' | 'one' | 'all')[] = ['none', 'all', 'one']
                const currentIndex = modes.indexOf(repeatMode)
                handleSetRepeat(modes[(currentIndex + 1) % modes.length])
              }}
              style={{
                padding: '0.5rem',
                background: 'transparent',
                border: 'none',
                cursor: 'pointer',
                fontSize: '1.25rem',
                opacity: repeatMode !== 'none' ? 1 : 0.5
              }}
            >
              {repeatMode === 'one' ? '🔂' : repeatMode === 'all' ? '🔁' : '🔁'}
            </button>
          </div>

          {/* Volume */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flex: 1, justifyContent: 'flex-end' }}>
            <span style={{ fontSize: '1.25rem' }}>🔊</span>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={volume}
              onChange={(e) => handleUpdateVolume(parseFloat(e.target.value))}
              style={{ width: '100px' }}
            />
          </div>
        </div>
      )}
    </div>
  )
}

export default MusicPlayer
