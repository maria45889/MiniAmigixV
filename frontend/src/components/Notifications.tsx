import React, { useState } from 'react';
import './Notifications.css';

interface Notification {
  id: number;
  icon: string;
  title: string;
  message: string;
  time: string;
  unread?: boolean;
}

const Notifications: React.FC = () => {
  const [activeFilter, setActiveFilter] = useState('Todas');

  const filters = [
    { id: 'Todas', label: 'Todas', count: 6 },
    { id: 'Sin Leer', label: 'Sin Leer', count: 3 },
    { id: 'Importantes', label: 'Importantes', count: 0 },
    { id: 'Eliminadas', label: 'Eliminadas', count: 0 },
  ];

  const notifications: Notification[] = [
    {
      id: 1,
      icon: '🤖',
      title: 'Respuesta de Amigis en Chat IA',
      message: 'Amigis respondió a tu pregunta sobre cómo construir una API REST en Django.',
      time: 'Hace 10 min',
      unread: true
    },
    {
      id: 2,
      icon: '🎓',
      title: '¡Tutorial Completado! (+60 XP)',
      message: 'Has finalizado el tutorial "HTML5 & CSS3 Moderno". ¡Desbloqueaste la insignia de Web Dev!',
      time: 'Hace 1 hora',
      unread: true
    },
    {
      id: 3,
      icon: '📅',
      title: 'Recordatorio de Evento Próximo',
      message: 'Tienes el evento "Examen de Matemáticas" programado para mañana a las 08:00 AM.',
      time: 'Hace 3 horas',
      unread: true
    },
    {
      id: 4,
      icon: '🎵',
      title: 'Nueva Playlist Recomendada',
      message: 'Amigis ha preparado la playlist "Lo-Fi para Estudiar" para ayudarte en tus sesiones de concentración.',
      time: 'Ayer',
      unread: false
    },
    {
      id: 5,
      icon: '🔄',
      title: 'MiniAmigixV 3.0 Ya Está Disponible',
      message: 'Disfruta del nuevo diseño Glassmorphic, traductor mejorado, visualizador de música y la Sala Arcade.',
      time: 'Hace 2 días',
      unread: false
    },
    {
      id: 6,
      icon: '📩',
      title: 'Mensaje del Sistema',
      message: 'Tu cuenta ha sido verificada con éxito. ¡Bienvenida a la comunidad!',
      time: 'Hace 3 días',
      unread: false
    }
  ];

  const filteredNotifications = notifications.filter(notification => {
    if (activeFilter === 'Todas') return true;
    if (activeFilter === 'Sin Leer') return notification.unread;
    return true;
  });

  return (
    <div className="notifications-container">
      <div className="notifications-header">
        <div className="header-title">
          <span className="header-icon">🔔</span>
          <div>
            <h1>Centro de Notificaciones</h1>
            <p>Entérate de mensajes, eventos próximos, nuevos logros y actualizaciones en tiempo real.</p>
          </div>
        </div>
        <div className="header-actions">
          <button className="action-btn secondary">✓ Marcar Todo Como Leído</button>
          <button className="action-btn secondary">🗑 Limpiar Notificaciones</button>
        </div>
      </div>

      {/* Filters */}
      <div className="filters-section">
        <div className="filters-grid">
          {filters.map((filter) => (
            <button
              key={filter.id}
              className={`filter-btn ${activeFilter === filter.id ? 'active' : ''}`}
              onClick={() => setActiveFilter(filter.id)}
            >
              {filter.label} ({filter.count})
            </button>
          ))}
        </div>
      </div>

      {/* Notifications List */}
      <div className="notifications-list">
        {filteredNotifications.map((notification) => (
          <div key={notification.id} className={`notification-item ${notification.unread ? 'unread' : ''}`}>
            <span className="notification-icon">{notification.icon}</span>
            <div className="notification-content">
              <h4>{notification.title}</h4>
              <p>{notification.message}</p>
              <span className="notification-time">{notification.time}</span>
            </div>
            <button className="delete-btn">✕</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Notifications;
