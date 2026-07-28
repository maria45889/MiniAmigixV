import { useState } from 'react'
import Header from './Header'
import Sidebar from './Sidebar'
import AmigisDashboard from './AmigisDashboard'
import StatsCards from './StatsCards'
import QuickActions from './QuickActions'
import WeeklyActivity from './WeeklyActivity'
import WeeklyGoals from './WeeklyGoals'
import TodayActivity from './TodayActivity'
import ChatLayout from './ChatLayout'
import MusicPlayer from './MusicPlayer'
import GamesHub from './GamesHub'
import Study from './Study'
import Entertainment from './Entertainment'
import Weather from './Weather'
import Translator from './Translator'
import Blog from './Blog'
import Events from './Events'
import Tutorials from './Tutorials'
import Files from './Files'
import AdminCenter from './AdminCenter'
import Profile from './Profile'
import Settings from './Settings'
import HelpCenter from './HelpCenter'
import Suggestions from './Suggestions'
import Notifications from './Notifications'

interface DashboardProps {
  username?: string
}

function Dashboard({ username = 'mariajosetacoc2005' }: DashboardProps) {
  const [activeItem, setActiveItem] = useState('Inicio')
  const [showProfileMenu, setShowProfileMenu] = useState(false)

  const handleNavigate = (item: string) => {
    setActiveItem(item)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    window.location.href = '/login'
  }

  const handleQuickAction = (action: string) => {
    // Handle quick action
  }

  return (
    <div style={{
      display: 'flex',
      width: '100%',
      gap: '0.5rem',
      padding: '0.25rem',
      minHeight: '100vh',
      background: 'var(--bg-dark, #0f172a)'
    }}>
      {/* Sidebar */}
      <Sidebar
        activeItem={activeItem}
        onNavigate={handleNavigate}
        onLogout={handleLogout}
      />

      {/* Main Content */}
      <main style={{ flex: 1, width: '100%', display: 'flex', flexDirection: 'column', gap: '0.375rem' }}>
        {/* Header */}
        <Header
          username={username}
          onLogout={handleLogout}
        />

        {/* Dashboard Content */}
        {activeItem === 'Inicio' && (
          <>
            {/* Amigis Welcome Message */}
            <AmigisDashboard username={username} />

            {/* Stats Cards */}
            <StatsCards />

            {/* Quick Actions */}
            <QuickActions onAction={handleQuickAction} />

            {/* Two Column Layout */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
              gap: '0.5rem'
            }}>
              {/* Weekly Activity */}
              <WeeklyActivity />

              {/* Weekly Goals */}
              <WeeklyGoals />
            </div>

            {/* Today Activity */}
            <TodayActivity />
          </>
        )}

        {/* Chat IA - Full Screen Layout */}
        {activeItem === 'Chat IA' && (
          <ChatLayout onBack={() => setActiveItem('Inicio')} />
        )}

        {/* Música - Full Screen Layout */}
        {activeItem === 'Música' && (
          <MusicPlayer />
        )}

        {/* Juegos - Full Screen Layout */}
        {activeItem === 'Juegos' && (
          <GamesHub />
        )}

        {/* Estudio - Full Screen Layout */}
        {activeItem === 'Estudio' && (
          <Study />
        )}

        {/* Entretenimiento - Full Screen Layout */}
        {activeItem === 'Entretenimiento' && (
          <Entertainment />
        )}

        {/* Clima - Full Screen Layout */}
        {activeItem === 'Clima' && (
          <Weather />
        )}

        {/* Traductor - Full Screen Layout */}
        {activeItem === 'Traductor' && (
          <Translator />
        )}

        {/* Blog - Full Screen Layout */}
        {activeItem === 'Blog' && (
          <Blog />
        )}

        {/* Eventos - Full Screen Layout */}
        {activeItem === 'Eventos' && (
          <Events />
        )}

        {/* Tutoriales - Full Screen Layout */}
        {activeItem === 'Tutoriales' && (
          <Tutorials />
        )}

        {/* Mis Archivos - Full Screen Layout */}
        {activeItem === 'Mis Archivos' && (
          <Files />
        )}

        {/* Centro Admin - Full Screen Layout */}
        {activeItem === 'Centro Admin' && (
          <AdminCenter />
        )}

        {/* Administración - Full Screen Layout */}
        {activeItem === 'Administración' && (
          <Profile />
        )}

        {/* Configuración - Full Screen Layout */}
        {activeItem === 'Configuración' && (
          <Settings />
        )}

        {/* Soporte - Full Screen Layout */}
        {activeItem === 'Soporte' && (
          <HelpCenter />
        )}

        {/* Sugerencias - Full Screen Layout */}
        {activeItem === 'Sugerencias' && (
          <Suggestions />
        )}

        {/* Notificaciones - Full Screen Layout */}
        {activeItem === 'Notificaciones' && (
          <Notifications />
        )}

        {/* Placeholder for other sections */}
        {activeItem !== 'Inicio' && activeItem !== 'Chat IA' && activeItem !== 'Música' && activeItem !== 'Juegos' && activeItem !== 'Estudio' && activeItem !== 'Entretenimiento' && activeItem !== 'Clima' && activeItem !== 'Traductor' && activeItem !== 'Blog' && activeItem !== 'Eventos' && activeItem !== 'Tutoriales' && activeItem !== 'Mis Archivos' && activeItem !== 'Centro Admin' && activeItem !== 'Administración' && activeItem !== 'Configuración' && activeItem !== 'Soporte' && activeItem !== 'Sugerencias' && activeItem !== 'Notificaciones' && (
          <div className="glass-panel" style={{
            padding: '3rem',
            textAlign: 'center',
            background: 'var(--glass-bg, rgba(255, 255, 255, 0.05))',
            backdropFilter: 'blur(10px)',
            border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
            borderRadius: '12px'
          }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>
              {activeItem === 'Música' && '🎵'}
              {activeItem === 'Juegos' && '🎮'}
              {activeItem === 'Estudio' && '📚'}
              {activeItem === 'Entretenimiento' && '🎬'}
              {activeItem === 'Clima' && '🌦️'}
              {activeItem === 'Traductor' && '🌐'}
              {activeItem === 'Blog' && '📝'}
              {activeItem === 'Eventos' && '📅'}
              {activeItem === 'Tutoriales' && '📖'}
              {activeItem === 'Mis Archivos' && '📁'}
              {activeItem === 'Administración' && '⚙️'}
              {activeItem === 'Centro Admin' && '🏛️'}
            </div>
            <h2 style={{
              fontSize: '1.5rem',
              fontWeight: 600,
              color: 'var(--text-primary, #e2e8f0)',
              marginBottom: '0.5rem'
            }}>
              {activeItem}
            </h2>
            <p style={{
              fontSize: '1rem',
              color: 'var(--text-secondary, #94a3b8)'
            }}>
              Esta sección está en desarrollo. Próximamente...
            </p>
          </div>
        )}
      </main>
    </div>
  )
}

export default Dashboard
