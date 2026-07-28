import { useState, useRef, useEffect } from 'react'

interface ChatInputProps {
  onSendMessage: (message: string) => void
}

function ChatInput({ onSendMessage }: ChatInputProps) {
  const [message, setMessage] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const handleSend = () => {
    if (message.trim()) {
      onSendMessage(message.trim())
      setMessage('')
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`
    }
  }, [message])

  return (
    <div style={{
      padding: '1rem',
      background: 'rgba(15, 23, 42, 0.95)',
      backdropFilter: 'blur(10px)',
      borderTop: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
      display: 'flex',
      alignItems: 'flex-end',
      flexShrink: 0
    }}>
      <div style={{
        width: '100%',
        display: 'flex',
        gap: '0.75rem',
        alignItems: 'flex-end'
      }}>
        {/* Textarea */}
        <div style={{
          flex: 1,
          position: 'relative',
          background: 'rgba(255, 255, 255, 0.05)',
          border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.2))',
          borderRadius: '12px',
          transition: 'border-color 0.2s, box-shadow 0.2s'
        }}>
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Escribe tu mensaje..."
            rows={1}
            style={{
              width: '100%',
              padding: '1rem 1.25rem',
              background: 'transparent',
              border: 'none',
              borderRadius: '12px',
              color: 'var(--text-primary, #e2e8f0)',
              fontSize: '0.95rem',
              lineHeight: '1.5',
              resize: 'none',
              outline: 'none',
              fontFamily: 'inherit',
              maxHeight: '200px',
              overflowY: 'auto'
            }}
            onFocus={(e) => {
              e.currentTarget.parentElement!.style.borderColor = '#06b6d4'
              e.currentTarget.parentElement!.style.boxShadow = '0 0 0 2px rgba(6, 182, 212, 0.2)'
            }}
            onBlur={(e) => {
              e.currentTarget.parentElement!.style.borderColor = 'var(--glass-border, rgba(255, 255, 255, 0.2))'
              e.currentTarget.parentElement!.style.boxShadow = 'none'
            }}
          />
        </div>

        {/* Send Button */}
        <button
          onClick={handleSend}
          disabled={!message.trim()}
          style={{
            width: '48px',
            height: '48px',
            background: message.trim()
              ? 'linear-gradient(135deg, #7c3aed, #06b6d4)'
              : 'rgba(255, 255, 255, 0.1)',
            border: message.trim()
              ? 'none'
              : '1px solid var(--glass-border, rgba(255, 255, 255, 0.2))',
            borderRadius: '12px',
            color: message.trim() ? 'white' : 'var(--text-secondary, #94a3b8)',
            cursor: message.trim() ? 'pointer' : 'not-allowed',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.2rem',
            transition: 'all 0.2s',
            opacity: message.trim() ? 1 : 0.5
          }}
          onMouseEnter={(e) => {
            if (message.trim()) {
              e.currentTarget.style.transform = 'translateY(-2px)'
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(124, 58, 237, 0.3)'
            }
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)'
            e.currentTarget.style.boxShadow = 'none'
          }}
        >
          ➤
        </button>
      </div>
    </div>
  )
}

export default ChatInput
