// ============================================================================
// LOGIN COMPONENT
// ============================================================================

import { useState } from 'react'

// ============================================================================
// TYPES
// ============================================================================

interface LoginProps {
  onRegister?: () => void
  onPasswordReset?: () => void
}

function Login({ onRegister, onPasswordReset }: LoginProps) {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    setMessage(null)

    try {
      const response = await fetch('http://127.0.0.1:8000/api/account/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      const data = await response.json()

      if (response.ok) {
        setMessage({ type: 'success', text: 'Inicio de sesión exitoso.' })
        // Guardar token y redirigir
        if (data.token) {
          localStorage.setItem('token', data.token)
        }
        setTimeout(() => {
          window.location.href = '/'
        }, 1000)
      } else {
        setMessage({ type: 'error', text: data.error || 'Usuario o contraseña incorrectos.' })
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Error de conexión con el servidor.' })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="auth-wrapper">
      <div className="config-card" style={{ maxWidth: '450px', width: '100%', padding: '2rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '12px', marginBottom: '1.5rem' }}>
          <img src="/favicon.svg" alt="MiniAmigixV Logo" style={{ width: '48px', height: '48px' }} />
          <h2 style={{ 
            fontSize: '1.8rem', 
            fontWeight: 'bold', 
            margin: 0,
            background: 'linear-gradient(135deg, #7c3aed, #06b6d4)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text'
          }}>
            MiniAmigixV
          </h2>
        </div>

        <h3 style={{ 
          textAlign: 'center', 
          marginBottom: '2rem', 
          fontSize: '1.4rem',
          color: 'var(--text-primary, #e2e8f0)'
        }}>
          Bienvenido de nuevo
        </h3>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1.2rem' }}>
            <label htmlFor="username" style={{ 
              display: 'block', 
              fontWeight: 500, 
              color: 'var(--text-primary, #e2e8f0)',
              marginBottom: '8px'
            }}>
              Usuario
            </label>
            <div style={{ position: 'relative' }}>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                placeholder="majo123"
                required
                style={{
                  width: '100%',
                  padding: '12px 12px 12px 40px',
                  background: 'rgba(0,0,0,0.2)',
                  border: '1px solid var(--glass-border, #2d3748)',
                  color: 'var(--text-primary, #f1f5f9)',
                  borderRadius: '8px',
                  fontSize: '1rem',
                  outline: 'none',
                  transition: 'border-color 0.2s, box-shadow 0.2s'
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = '#06b6d4'
                  e.target.style.boxShadow = '0 0 0 2px rgba(6, 182, 212, 0.2)'
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = 'var(--glass-border, #2d3748)'
                  e.target.style.boxShadow = 'none'
                }}
              />
              <span style={{ 
                position: 'absolute', 
                left: '12px', 
                top: '50%', 
                transform: 'translateY(-50%)',
                fontSize: '1.2rem'
              }}>
                👤
              </span>
            </div>
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <label htmlFor="password" style={{ 
              display: 'block', 
              fontWeight: 500, 
              color: 'var(--text-primary, #e2e8f0)',
              marginBottom: '8px'
            }}>
              Contraseña
            </label>
            <div style={{ position: 'relative' }}>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="••••••••••••"
                required
                style={{
                  width: '100%',
                  padding: '12px 12px 12px 40px',
                  background: 'rgba(0,0,0,0.2)',
                  border: '1px solid var(--glass-border, #2d3748)',
                  color: 'var(--text-primary, #f1f5f9)',
                  borderRadius: '8px',
                  fontSize: '1rem',
                  outline: 'none',
                  transition: 'border-color 0.2s, box-shadow 0.2s'
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = '#06b6d4'
                  e.target.style.boxShadow = '0 0 0 2px rgba(6, 182, 212, 0.2)'
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = 'var(--glass-border, #2d3748)'
                  e.target.style.boxShadow = 'none'
                }}
              />
              <span style={{ 
                position: 'absolute', 
                left: '12px', 
                top: '50%', 
                transform: 'translateY(-50%)',
                fontSize: '1.2rem'
              }}>
                🔒
              </span>
            </div>
          </div>

          {message && (
            <div style={{
              background: message.type === 'success' 
                ? 'rgba(16, 185, 129, 0.1)' 
                : 'rgba(239, 68, 68, 0.1)',
              border: `1px solid ${message.type === 'success' 
                ? 'rgba(16, 185, 129, 0.3)' 
                : 'rgba(239, 68, 68, 0.3)'}`,
              padding: '12px',
              borderRadius: '8px',
              marginBottom: '1rem',
              color: message.type === 'success' ? '#34d399' : '#fca5a5',
              fontSize: '0.9rem'
            }}>
              {message.text}
            </div>
          )}

          <button
            type="submit"
            disabled={isSubmitting}
            style={{
              width: '100%',
              padding: '12px',
              marginTop: '10px',
              background: 'linear-gradient(135deg, #7c3aed, #06b6d4)',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontWeight: 600,
              cursor: isSubmitting ? 'not-allowed' : 'pointer',
              transition: 'transform 0.2s, box-shadow 0.2s',
              opacity: isSubmitting ? 0.7 : 1
            }}
            onMouseEnter={(e) => {
              if (!isSubmitting) {
                e.currentTarget.style.transform = 'translateY(-2px)'
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(124, 58, 237, 0.3)'
              }
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)'
              e.currentTarget.style.boxShadow = 'none'
            }}
          >
            {isSubmitting ? 'Entrando...' : 'Entrar'}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: '1rem' }}>
          <button
            onClick={onPasswordReset}
            style={{
              background: 'none',
              border: 'none',
              color: '#06b6d4',
              fontSize: '0.9rem',
              cursor: 'pointer',
              textDecoration: 'none',
              transition: 'color 0.2s'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.color = '#7c3aed'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.color = '#06b6d4'
            }}
          >
            ¿Olvidaste tu contraseña?
          </button>
        </div>
        
        <p style={{ textAlign: 'center', marginTop: '1.5rem', color: 'var(--text-secondary, #94a3b8)', fontSize: '0.9rem' }}>
          ¿No tienes cuenta?{' '}
          <button
            onClick={onRegister}
            style={{
              background: 'none',
              border: 'none',
              color: '#06b6d4',
              fontSize: '0.9rem',
              fontWeight: 600,
              cursor: 'pointer',
              textDecoration: 'none',
              transition: 'color 0.2s'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.color = '#7c3aed'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.color = '#06b6d4'
            }}
          >
            Regístrate aquí
          </button>
        </p>
      </div>
    </div>
  )
}

export default Login
