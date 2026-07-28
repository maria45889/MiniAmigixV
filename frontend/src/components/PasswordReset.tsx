import { useState } from 'react'

interface PasswordResetProps {
  onBack?: () => void
}

function PasswordReset({ onBack }: PasswordResetProps) {
  const [email, setEmail] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    setMessage(null)

    try {
      const response = await fetch('http://127.0.0.1:8000/api/account/reset-password/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      })

      const data = await response.json()

      if (response.ok) {
        setMessage({ type: 'success', text: 'Se ha enviado un enlace a tu correo electrónico.' })
        setEmail('')
      } else {
        setMessage({ type: 'error', text: data.error || 'Error al procesar la solicitud.' })
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
        <h2 style={{ 
          textAlign: 'center', 
          marginBottom: '1rem', 
          fontSize: '1.8rem',
          background: 'linear-gradient(135deg, #7c3aed, #06b6d4)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text'
        }}>
          Recuperar Contraseña
        </h2>
        
        <p style={{ 
          textAlign: 'center', 
          color: 'var(--text-secondary, #94a3b8)', 
          marginBottom: '2rem', 
          fontSize: '0.95rem',
          lineHeight: '1.5'
        }}>
          ¿Has olvidado tu contraseña? Introduce tu correo electrónico y te enviaremos un enlace para crear una nueva.
        </p>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1.5rem' }}>
            <label htmlFor="email" style={{ 
              display: 'block', 
              fontWeight: 500, 
              color: 'var(--text-primary, #e2e8f0)',
              marginBottom: '8px'
            }}>
              Correo electrónico
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="tu@correo.com"
              required
              style={{
                width: '100%',
                padding: '12px',
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
            {isSubmitting ? 'Enviando...' : 'Restablecer contraseña'}
          </button>
        </form>
        
        <p style={{ textAlign: 'center', marginTop: '2rem' }}>
          <button
            onClick={onBack}
            style={{
              background: 'none',
              border: 'none',
              color: 'var(--text-secondary, #94a3b8)',
              fontSize: '0.9rem',
              cursor: 'pointer',
              transition: 'color 0.2s'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.color = 'var(--text-primary, #e2e8f0)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.color = 'var(--text-secondary, #94a3b8)'
            }}
          >
            ← Volver a Iniciar Sesión
          </button>
        </p>
      </div>
    </div>
  )
}

export default PasswordReset
