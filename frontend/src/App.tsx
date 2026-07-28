// ============================================================================
// APP COMPONENT
// ============================================================================

import { useState } from 'react'
import { ThemeProvider } from './contexts/ThemeContext'
import Dashboard from './components/Dashboard'
import Login from './components/Login'
import PasswordReset from './components/PasswordReset'
import Register from './components/Register'

import './index.css'

// ============================================================================
// TYPES
// ============================================================================

type AuthView = 'login' | 'register' | 'password-reset' | 'dashboard'

// ============================================================================
// COMPONENT
// ============================================================================

function App() {
  const [authView, setAuthView] = useState<AuthView>('dashboard')

  const renderAuthView = () => {
    switch (authView) {
      case 'login':
        return (
          <Login
            onRegister={() => setAuthView('register')}
            onPasswordReset={() => setAuthView('password-reset')}
          />
        )
      case 'register':
        return <Register onLogin={() => setAuthView('login')} />
      case 'password-reset':
        return <PasswordReset onBack={() => setAuthView('login')} />
      case 'dashboard':
        return <Dashboard username="mariajosetacoc2005" />
      default:
        return (
          <Login
            onRegister={() => setAuthView('register')}
            onPasswordReset={() => setAuthView('password-reset')}
          />
        )
    }
  }

  return (
    <ThemeProvider>
      <div className="app-container">
        {renderAuthView()}
      </div>
    </ThemeProvider>
  )
}

export default App
