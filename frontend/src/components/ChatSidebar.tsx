interface Conversation {
  id: string
  title: string
  lastMessage: string
  timestamp: Date
}

interface ChatSidebarProps {
  conversations: Conversation[]
  currentConversation: string
  isOpen: boolean
  onNewConversation: () => void
  onSelectConversation: (id: string) => void
  onToggle: () => void
  onBack?: () => void
}

function ChatSidebar({
  conversations,
  currentConversation,
  isOpen,
  onNewConversation,
  onSelectConversation,
  onToggle,
  onBack
}: ChatSidebarProps) {
  return (
    <aside style={{
      width: isOpen ? '280px' : '80px',
      minWidth: isOpen ? '280px' : '80px',
      maxWidth: isOpen ? '280px' : '80px',
      height: '100%',
      background: 'var(--glass-bg, rgba(30, 41, 59, 0.95))',
      backdropFilter: 'blur(10px)',
      borderRight: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
      display: 'flex',
      flexDirection: 'column',
      transition: 'width 0.3s ease, min-width 0.3s ease, max-width 0.3s ease',
      overflow: 'hidden'
    }}>
      {/* Header */}
      <div style={{
        padding: isOpen ? '1rem' : '0.75rem',
        borderBottom: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))',
        display: 'flex',
        alignItems: 'center',
        justifyContent: isOpen ? 'space-between' : 'center',
        gap: '0.5rem'
      }}>
        {isOpen && (
          <button
            onClick={onNewConversation}
            style={{
              flex: 1,
              padding: '0.75rem 1rem',
              background: 'linear-gradient(135deg, #7c3aed, #06b6d4)',
              border: 'none',
              borderRadius: '8px',
              color: 'white',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              fontSize: '0.9rem',
              transition: 'transform 0.2s, box-shadow 0.2s'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)'
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(124, 58, 237, 0.3)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)'
              e.currentTarget.style.boxShadow = 'none'
            }}
          >
            <span>+</span>
            <span>Nueva</span>
          </button>
        )}

        <button
          onClick={onToggle}
          style={{
            width: '36px',
            height: '36px',
            background: 'rgba(255, 255, 255, 0.1)',
            border: '1px solid var(--glass-border, rgba(255, 255, 255, 0.2))',
            borderRadius: '8px',
            color: 'var(--text-primary, #e2e8f0)',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.2rem',
            transition: 'background 0.2s'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = 'rgba(255, 255, 255, 0.1)'
          }}
        >
          {isOpen ? '◀' : '▶'}
        </button>
      </div>

      {/* Conversations List */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: isOpen ? '0.5rem' : '0.5rem'
      }}>
        {conversations.map((conv) => (
          <button
            key={conv.id}
            onClick={() => onSelectConversation(conv.id)}
            style={{
              width: '100%',
              padding: isOpen ? '0.75rem 1rem' : '0.75rem',
              background: currentConversation === conv.id
                ? 'rgba(124, 58, 237, 0.2)'
                : 'transparent',
              border: currentConversation === conv.id
                ? '1px solid rgba(124, 58, 237, 0.3)'
                : '1px solid transparent',
              borderRadius: '8px',
              cursor: 'pointer',
              transition: 'all 0.2s',
              marginBottom: '0.25rem',
              textAlign: 'left',
              overflow: 'hidden'
            }}
            onMouseEnter={(e) => {
              if (currentConversation !== conv.id) {
                e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)'
              }
            }}
            onMouseLeave={(e) => {
              if (currentConversation !== conv.id) {
                e.currentTarget.style.background = 'transparent'
              }
            }}
          >
            {isOpen ? (
              <>
                <div style={{
                  fontSize: '0.9rem',
                  fontWeight: 500,
                  color: 'var(--text-primary, #e2e8f0)',
                  marginBottom: '0.25rem',
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis'
                }}>
                  {conv.title}
                </div>
                <div style={{
                  fontSize: '0.8rem',
                  color: 'var(--text-secondary, #94a3b8)',
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis'
                }}>
                  {conv.lastMessage}
                </div>
              </>
            ) : (
              <div style={{
                width: '36px',
                height: '36px',
                borderRadius: '50%',
                background: currentConversation === conv.id
                  ? 'linear-gradient(135deg, #7c3aed, #06b6d4)'
                  : 'rgba(255, 255, 255, 0.1)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '1rem',
                margin: '0 auto'
              }}>
                💬
              </div>
            )}
          </button>
        ))}
      </div>

      {/* Footer */}
      <div style={{
        padding: isOpen ? '1rem' : '0.75rem',
        borderTop: '1px solid var(--glass-border, rgba(255, 255, 255, 0.1))'
      }}>
        {isOpen ? (
          <button
            onClick={onBack}
            style={{
              width: '100%',
              padding: '0.75rem 1rem',
              background: 'transparent',
              border: '1px solid #ef4444',
              borderRadius: '8px',
              color: '#ef4444',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.5rem',
              fontSize: '0.9rem',
              transition: 'all 0.2s'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'rgba(239, 68, 68, 0.1)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent'
            }}
          >
            ← Volver
          </button>
        ) : (
          <button
            onClick={onBack}
            style={{
              width: '36px',
              height: '36px',
              background: 'rgba(239, 68, 68, 0.1)',
              border: '1px solid #ef4444',
              borderRadius: '8px',
              color: '#ef4444',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1rem',
              margin: '0 auto',
              transition: 'background 0.2s'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'rgba(239, 68, 68, 0.2)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'rgba(239, 68, 68, 0.1)'
            }}
          >
            ←
          </button>
        )}
      </div>
    </aside>
  )
}

export default ChatSidebar
