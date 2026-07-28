import React, { useState } from 'react';
import './HelpCenter.css';

interface FAQ {
  id: number;
  question: string;
  answer: string;
}

const HelpCenter: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');

  const faqs: FAQ[] = [
    {
      id: 1,
      question: '¿Cómo cambiar mi contraseña?',
      answer: 'Dirígete al módulo de Configuración ➔ Privacidad o a la sección de tu Perfil para actualizar tu clave de acceso de forma segura.'
    },
    {
      id: 2,
      question: '¿Cómo instalar la aplicación (PWA)?',
      answer: 'Abre la app en Chrome o Edge y haz clic en "Instalar MiniAmigixV" en la barra de navegación para tener el acceso directo en tu escritorio.'
    },
    {
      id: 3,
      question: '¿Cómo sincronizar mis datos?',
      answer: 'Tus progresos de estudio, chats y configuraciones se guardan automáticamente en tu cuenta sincronizada en la nube.'
    },
    {
      id: 4,
      question: '¿Cómo funciona Amigis?',
      answer: 'Amigis es tu compañero IA inteligente. Responde dudas, recomienda canciones, organiza tus eventos y te acompaña en los minijuegos.'
    },
    {
      id: 5,
      question: '¿Cómo crear una playlist?',
      answer: 'En el módulo de Música, haz clic en "+ Nueva Playlist", dale un nombre y agrega tus canciones favoritas fácilmente.'
    },
    {
      id: 6,
      question: '¿Cómo exportar mis archivos?',
      answer: 'En el módulo Mis Archivos o en Configuración ➔ Copias de seguridad puedes descargar tus datos en formato PDF o JSON.'
    }
  ];

  const diagnosticItems = [
    { id: 1, name: 'Conexión', icon: '🌐', status: 'Pendiente' },
    { id: 2, name: 'Cuenta', icon: '🔑', status: 'Pendiente' },
    { id: 3, name: 'Sincronización', icon: '☁', status: 'Pendiente' },
    { id: 4, name: 'Espacio', icon: '💾', status: 'Pendiente' },
    { id: 5, name: 'Notificaciones', icon: '🔔', status: 'Pendiente' },
    { id: 6, name: 'Configuración', icon: '⚙️', status: 'Pendiente' },
  ];

  const systemServices = [
    { name: 'Servicio IA Chat', status: 'En línea' },
    { name: 'Reproductor Música', status: 'En línea' },
    { name: 'Servicio Clima API', status: 'En línea' },
    { name: 'Motor Traductor', status: 'En línea' },
  ];

  return (
    <div className="help-center-container">
      <div className="help-header">
        <div className="header-title">
          <span className="header-icon">🆘</span>
          <div>
            <h1>Centro de Ayuda & Soporte</h1>
            <p>¿En qué podemos ayudarte hoy? Encuentra respuestas, guías o contacta al equipo.</p>
          </div>
        </div>
      </div>

      {/* Search and Actions */}
      <div className="search-section">
        <div className="search-bar">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder="Buscar ayuda..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <div className="action-buttons">
            <button className="action-btn primary">🔧 Diagnóstico</button>
            <button className="action-btn secondary">📢 Reportar Problema</button>
            <button className="action-btn secondary">💡 Sugerencias</button>
          </div>
        </div>
      </div>

      {/* Diagnostics */}
      <div className="diagnostics-section">
        <div className="diagnostics-card">
          <div className="diagnostics-header">
            <span className="badge">IDEAS EXCLUSIVAS • AMIGIS DIAGNOSTICS</span>
            <h3>🔧 Diagnóstico Inteligente de MiniAmigixV</h3>
            <p>Haz clic en el botón para verificar el estado de tu cuenta, conexión, espacio y notificaciones.</p>
          </div>
          <button className="diagnostics-btn">⚡ Ejecutar Diagnóstico</button>
          <div className="diagnostics-grid">
            {diagnosticItems.map((item) => (
              <div key={item.id} className="diagnostic-item">
                <span className="diagnostic-icon">{item.icon}</span>
                <span className="diagnostic-name">{item.name}</span>
                <span className="diagnostic-status">{item.status}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* FAQ */}
      <div className="faq-section">
        <div className="section-header">
          <h3>Preguntas Frecuentes (FAQ)</h3>
        </div>
        <div className="faq-list">
          {faqs.map((faq) => (
            <div key={faq.id} className="faq-item">
              <h4>{faq.question}</h4>
              <p>{faq.answer}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Report Problem */}
      <div className="report-section">
        <div className="section-header">
          <h3>Reportar un Problema / Ticket</h3>
        </div>
        <div className="form-card">
          <div className="form-group">
            <label>Título del problema</label>
            <input type="text" placeholder="Ej. Error al reproducir audio" />
          </div>
          <div className="form-group">
            <label>Categoría</label>
            <select defaultValue="🤖 IA Chat">
              <option>🤖 IA Chat</option>
              <option>🎵 Música</option>
              <option>🎮 Juegos</option>
              <option>📚 Estudio</option>
              <option>🌤️ Clima</option>
              <option>🌐 Traductor</option>
              <option>📁 Archivos</option>
              <option>⚙️ Cuenta</option>
            </select>
          </div>
          <div className="form-group">
            <label>Prioridad</label>
            <select defaultValue="Media">
              <option>Baja</option>
              <option>Media</option>
              <option>Alta</option>
              <option>Crítica</option>
            </select>
          </div>
          <div className="form-group">
            <label>Descripción detallada</label>
            <textarea placeholder="Explica qué sucedió y cómo podemos reproducir el fallo..." rows={4} />
          </div>
          <button className="action-btn primary">📤 Enviar Reporte de Soporte</button>
        </div>
      </div>

      {/* Suggestion */}
      <div className="suggestion-section">
        <div className="section-header">
          <h3>Enviar una Sugerencia / Idea</h3>
        </div>
        <div className="form-card">
          <div className="form-group">
            <label>✨ Nueva función</label>
            <input type="text" placeholder="Título de tu idea" />
          </div>
          <div className="form-group">
            <label>Describe tu sugerencia para mejorar MiniAmigixV...</label>
            <textarea rows={4} />
          </div>
          <button className="action-btn primary">💡 Enviar Idea al Equipo</button>
        </div>
      </div>

      {/* System Status */}
      <div className="system-status-section">
        <div className="section-header">
          <h3>Estado del Sistema</h3>
        </div>
        <div className="status-card">
          <div className="status-message">
            <span className="status-indicator">🟢</span>
            <span>Todos los servicios funcionando al 100%.</span>
          </div>
          <div className="services-list">
            {systemServices.map((service, index) => (
              <div key={index} className="service-item">
                <span className="service-name">{service.name}</span>
                <span className="service-status online">En línea</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Chat Assistance */}
      <div className="chat-assistance-section">
        <div className="chat-card">
          <div className="chat-header">
            <span className="chat-icon">💬</span>
            <h3>Chat de Asistencia Amigis</h3>
          </div>
          <p>"Hola 👋 Soy Amigis. Puedo guiarte paso a paso o responder cualquier pregunta sobre la app."</p>
          <button className="action-btn primary">💬 Iniciar Conversación en Chat IA</button>
        </div>
      </div>

      {/* Contact Channels */}
      <div className="contact-section">
        <div className="section-header">
          <h3>📞 Canales de Contacto</h3>
        </div>
        <div className="contact-grid">
          <div className="contact-card">
            <span className="contact-icon">📧</span>
            <span className="contact-label">Correo</span>
            <span className="contact-value">soporte@miniamigixv.com</span>
          </div>
          <div className="contact-card">
            <span className="contact-icon">🌐</span>
            <span className="contact-label">Web</span>
            <span className="contact-value">miniamigixv.app</span>
          </div>
          <div className="contact-card">
            <span className="contact-icon">📱</span>
            <span className="contact-label">Redes</span>
            <span className="contact-value">@miniamigixv</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HelpCenter;
