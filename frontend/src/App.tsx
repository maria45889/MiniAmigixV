import { useState } from 'react'
import './index.css'
import { ThemeProvider } from './contexts/ThemeContext'
import Dashboard from './components/Dashboard'
import Login from './components/Login'
import Register from './components/Register'
import PasswordReset from './components/PasswordReset'

type AuthView = 'login' | 'register' | 'password-reset' | 'dashboard'

function App() {
  const [authView, setAuthView] = useState<AuthView>('dashboard')

  const renderAuthView = () => {
    switch (authView) {
      case 'login':
        return <Login onRegister={() => setAuthView('register')} onPasswordReset={() => setAuthView('password-reset')} />
      case 'register':
        return <Register onLogin={() => setAuthView('login')} />
      case 'password-reset':
        return <PasswordReset onBack={() => setAuthView('login')} />
      case 'dashboard':
        return <Dashboard username="mariajosetacoc2005" />
      default:
        return <Login onRegister={() => setAuthView('register')} onPasswordReset={() => setAuthView('password-reset')} />
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
