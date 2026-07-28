import { useEffect, useRef } from 'react'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface ChatAreaProps {
  messages: Message[]
}

function ChatArea({ messages }: ChatAreaProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  return (
    <div style={{
      flex: 1,
      overflowY: 'auto',
      padding: '1rem',
      display: 'flex',
      flexDirection: 'column',
      gap: '1rem',
      background: 'transparent',
      scrollBehavior: 'smooth'
    }}>
      {/* Welcome Message */}
      {messages.length === 0 && (
        <div style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          padding: '2rem'
        }}>
          <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>🦆</div>
          <h2 style={{
            fontSize: '1.8rem',
            fontWeight: 600,
            color: 'var(--text-primary, #e2e8f0)',
            marginBottom: '0.5rem'
          }}>
            Bienvenido a Amigis IA
          </h2>
          <p style={{
            fontSize: '1rem',
            color: 'var(--text-secondary, #94a3b8)',
            maxWidth: '500px'
          }}>
            Soy tu asistente inteligente. ¿En qué puedo ayudarte hoy?
          </p>
        </div>
      )}

      {/* Messages */}
      {messages.map((message) => (
        <div
          key={message.id}
          style={{
            display: 'flex',
            justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
            width: '100%',
            padding: '0 1rem'
          }}
        >
          <div style={{
            width: '100%',
            display: 'flex',
            gap: '1rem',
            alignItems: 'flex-start',
            flexDirection: message.role === 'user' ? 'row-reverse' : 'row'
          }}>
            {/* Avatar */}
            <div style={{
              width: '40px',
              height: '40px',
              borderRadius: '50%',
              background: message.role === 'user'
                ? 'linear-gradient(135deg, #7c3aed, #06b6d4)'
                : 'linear-gradient(135deg, #10b981, #06b6d4)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.2rem',
              flexShrink: 0
            }}>
              {message.role === 'user' ? '👤' : '🦆'}
            </div>

            {/* Message Content */}
            <div style={{
              flex: 1,
              display: 'flex',
              flexDirection: 'column',
              gap: '0.5rem',
              alignItems: message.role === 'user' ? 'flex-end' : 'flex-start'
            }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                flexDirection: message.role === 'user' ? 'row-reverse' : 'row'
              }}>
                <span style={{
                  fontSize: '0.95rem',
                  fontWeight: 600,
                  color: 'var(--text-primary, #e2e8f0)'
                }}>
                  {message.role === 'user' ? 'Tú' : 'Amigis IA'}
                </span>
                <span style={{
                  fontSize: '0.75rem',
                  color: 'var(--text-secondary, #94a3b8)'
                }}>
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>

              <div style={{
                padding: '1rem 1.25rem',
                background: message.role === 'user'
                  ? 'rgba(124, 58, 237, 0.15)'
                  : 'rgba(16, 185, 129, 0.1)',
                border: message.role === 'user'
                  ? '1px solid rgba(124, 58, 237, 0.3)'
                  : '1px solid rgba(16, 185, 129, 0.2)',
                borderRadius: message.role === 'user' ? '12px 12px 0 12px' : '12px 12px 12px 0',
                color: 'var(--text-primary, #e2e8f0)',
                fontSize: '0.95rem',
                lineHeight: '1.6',
                wordBreak: 'break-word',
                textAlign: 'left'
              }}>
                {message.content}
              </div>
            </div>
          </div>
        </div>
      ))}

      {/* Scroll to bottom */}
      <div ref={messagesEndRef} />
    </div>
  )
}

export default ChatArea
