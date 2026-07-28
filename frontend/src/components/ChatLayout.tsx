import { useState } from 'react'
import ChatSidebar from './ChatSidebar'
import ChatArea from './ChatArea'
import ChatInput from './ChatInput'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface Conversation {
  id: string
  title: string
  lastMessage: string
  timestamp: Date
}

interface ChatLayoutProps {
  onBack?: () => void
}

function ChatLayout({ onBack }: ChatLayoutProps) {

  const [conversations, setConversations] = useState<Conversation[]>([
    { id: '1', title: 'Consulta sobre APIs Django', lastMessage: '¿Cómo implementar REST?', timestamp: new Date() },
    { id: '2', title: 'Ayuda con React', lastMessage: 'Hooks personalizados', timestamp: new Date() },
    { id: '3', title: 'Traducción inglés-español', lastMessage: 'Hello world', timestamp: new Date() },
  ])

  const [currentConversation, setCurrentConversation] = useState<string>('1')
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', role: 'user', content: 'Hola, ¿puedes ayudarme con Django REST Framework?', timestamp: new Date() },
    { id: '2', role: 'assistant', content: '¡Claro! Django REST Framework es un toolkit poderoso para construir APIs web. ¿Qué específicamente necesitas saber?', timestamp: new Date() },
    { id: '3', role: 'user', content: '¿Cómo crear un ViewSet básico?', timestamp: new Date() },
  ])

  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  const handleSendMessage = (content: string) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date()
    }
    setMessages([...messages, newMessage])

    // Simular respuesta de IA
    setTimeout(() => {
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Entiendo tu pregunta. Déjame ayudarte con eso...',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, aiResponse])
    }, 1000)
  }

  const handleNewConversation = () => {
    const newConv: Conversation = {
      id: Date.now().toString(),
      title: 'Nueva conversación',
      lastMessage: '',
      timestamp: new Date()
    }
    setConversations([newConv, ...conversations])
    setCurrentConversation(newConv.id)
    setMessages([])
  }

  const handleSelectConversation = (id: string) => {
    setCurrentConversation(id)
  }

  return (
    <div style={{
      display: 'flex',
      height: '100%',
      width: '100%',
      background: 'var(--bg-dark, #0f172a)',
      overflow: 'hidden'
    }}>
      {/* Sidebar */}
      <ChatSidebar
        conversations={conversations}
        currentConversation={currentConversation}
        isOpen={isSidebarOpen}
        onNewConversation={handleNewConversation}
        onSelectConversation={handleSelectConversation}
        onToggle={() => setIsSidebarOpen(!isSidebarOpen)}
        onBack={onBack}
      />

      {/* Main Chat Area */}
      <div style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        overflow: 'hidden',
        background: 'linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)',
        alignItems: 'flex-start'
      }}>
        {/* Chat Messages */}
        <div style={{
          width: '100%',
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
          padding: '1rem'
        }}>
          <ChatArea messages={messages} />

          {/* Chat Input */}
          <ChatInput onSendMessage={handleSendMessage} />
        </div>
      </div>
    </div>
  )
}

export default ChatLayout
