// ============================================================================
// REGISTER COMPONENT
// ============================================================================

import { useState } from 'react'

// ============================================================================
// TYPES
// ============================================================================

interface RegisterProps {
  onLogin?: () => void
}

function Register({ onLogin }: RegisterProps) {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
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

    // Validación de contraseñas
    if (formData.password !== formData.confirmPassword) {
      setMessage({ type: 'error', text: 'Las contraseñas no coinciden.' })
      setIsSubmitting(false)
      return
    }

    if (formData.password.length < 8) {
      setMessage({ type: 'error', text: 'La contraseña debe tener al menos 8 caracteres.' })
      setIsSubmitting(false)
      return
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/api/account/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          password: formData.password
        }),
      })

      const data = await response.json()

      if (response.ok) {
        setMessage({ type: 'success', text: 'Cuenta creada exitosamente. Redirigiendo...' })
        setTimeout(() => {
          onLogin?.()
        }, 2000)
      } else {
        setMessage({ type: 'error', text: data.error || 'Error al crear la cuenta.' })
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Error de conexión con el servidor.' })
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleGoogleRegister = () => {
    // Redirigir a OAuth de Google
    window.location.href = 'http://127.0.0.1:8000/accounts/google/login/'
  }

  return (
    <div className="auth-wrapper">
      <div className="config-card" style={{ maxWidth: '450px', width: '100%', padding: '2rem' }}>
        <h2 style={{ 
          textAlign: 'center', 
          marginBottom: '1.5rem', 
          fontSize: '1.8rem',
          background: 'linear-gradient(135deg, #7c3aed, #06b6d4)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text'
        }}>
          MiniAmigixV
        </h2>

        <h3 style={{ 
          textAlign: 'center', 
          marginBottom: '1.5rem', 
          fontSize: '1.4rem',
          color: 'var(--text-primary, #e2e8f0)'
        }}>
          Crear cuenta
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
                placeholder="👤"
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

          <div style={{ marginBottom: '1.2rem' }}>
            <label htmlFor="email" style={{ 
              display: 'block', 
              fontWeight: 500, 
              color: 'var(--text-primary, #e2e8f0)',
              marginBottom: '8px'
            }}>
              Email
            </label>
            <div style={{ position: 'relative' }}>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="📧"
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
                📧
              </span>
            </div>
          </div>

          <div style={{ marginBottom: '1.2rem' }}>
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
                placeholder="🔒"
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

          <div style={{ marginBottom: '1.5rem' }}>
            <label htmlFor="confirmPassword" style={{ 
              display: 'block', 
              fontWeight: 500, 
              color: 'var(--text-primary, #e2e8f0)',
              marginBottom: '8px'
            }}>
              Confirmar Contraseña
            </label>
            <div style={{ position: 'relative' }}>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder="🔐"
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
                🔐
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
            {isSubmitting ? 'Registrando...' : 'Registrarse'}
          </button>
        </form>

        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          margin: '1.5rem 0',
          gap: '1rem'
        }}>
          <div style={{ flex: 1, height: '1px', background: 'var(--glass-border, #2d3748)' }}></div>
          <span style={{ color: 'var(--text-secondary, #94a3b8)', fontSize: '0.9rem' }}>O</span>
          <div style={{ flex: 1, height: '1px', background: 'var(--glass-border, #2d3748)' }}></div>
        </div>

        <button
          onClick={handleGoogleRegister}
          style={{
            width: '100%',
            padding: '12px',
            background: 'white',
            color: '#333',
            border: '1px solid #ddd',
            borderRadius: '8px',
            fontWeight: 600,
            cursor: 'pointer',
            transition: 'transform 0.2s, box-shadow 0.2s',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '10px'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-2px)'
            e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)'
            e.currentTarget.style.boxShadow = 'none'
          }}
        >
          <svg width="20" height="20" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          Registrarse con Google
        </button>
        
        <p style={{ textAlign: 'center', marginTop: '1.5rem', color: 'var(--text-secondary, #94a3b8)', fontSize: '0.9rem' }}>
          ¿Ya tienes cuenta?{' '}
          <button
            onClick={onLogin}
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
            Inicia sesión aquí
          </button>
        </p>
      </div>
    </div>
  )
}

export default Register
