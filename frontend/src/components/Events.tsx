import React, { useState } from 'react';
import './Events.css';

interface Event {
  id: number;
  title: string;
  icon: string;
  date: string;
  time: string;
  location: string;
  category: string;
}

interface Reminder {
  id: number;
  title: string;
  icon: string;
  date: string;
  time: string;
}

const Events: React.FC = () => {
  const [currentMonth, setCurrentMonth] = useState('Julio 2026');
  const [activeCategory, setActiveCategory] = useState('Todos');
  const [searchQuery, setSearchQuery] = useState('');

  const categories = [
    { id: 'Todos', name: 'Todos', icon: '📅' },
    { id: 'trabajo', name: 'Trabajo', icon: '💼' },
    { id: 'estudio', name: 'Estudio', icon: '📚' },
    { id: 'personal', name: 'Personal', icon: '👤' },
    { id: 'salud', name: 'Salud', icon: '💧' },
    { id: 'viajes', name: 'Viajes', icon: '✈️' },
    { id: 'ocio', name: 'Ocio', icon: '🎉' },
  ];

  const stats = [
    { icon: '📅', label: 'Eventos este mes', value: 4 },
    { icon: '⏰', label: 'Recordatorios activos', value: 4 },
    { icon: '✅', label: 'Eventos completados', value: 0 },
    { icon: '⭐', label: 'Tareas pendientes', value: 1 },
  ];

  const upcomingEvents: Event[] = [
    {
      id: 1,
      title: 'Entrega Proyecto de Software',
      icon: '📚',
      date: '25 jul',
      time: '10:00',
      location: 'Universidad',
      category: 'estudio'
    },
    {
      id: 2,
      title: 'Cumpleaños de un Amigo 🎂',
      icon: '🎉',
      date: '26 jul',
      time: '18:00',
      location: 'Casa',
      category: 'ocio'
    },
    {
      id: 3,
      title: 'Reunión de Trabajo',
      icon: '💼',
      date: 'Mañana',
      time: '09:00',
      location: 'Google Meet',
      category: 'trabajo'
    },
    {
      id: 4,
      title: 'Examen de Matemáticas',
      icon: '📚',
      date: '30 jul',
      time: '08:00',
      location: 'Aula 304',
      category: 'estudio'
    }
  ];

  const activeReminders: Reminder[] = [
    {
      id: 1,
      title: 'Estudiar Java',
      icon: '⏰',
      date: 'Hoy',
      time: '7:00 PM'
    },
    {
      id: 2,
      title: 'Leer documentación Django',
      icon: '📖',
      date: 'Hoy',
      time: '8:30 PM'
    },
    {
      id: 3,
      title: 'Tomar agua',
      icon: '💧',
      date: 'Cada 2 horas',
      time: ''
    },
    {
      id: 4,
      title: 'Revisar MiniAmigixV',
      icon: '💻',
      date: 'Mañana',
      time: ''
    }
  ];

  const calendarDays = [
    29, 30, 1, 2, 3, 4, 5,
    6, 7, 8, 9, 10, 11, 12,
    13, 14, 15, 16, 17, 18, 19,
    20, 21, 22, 23, 24, 25, 26,
    27, 28, 29, 30, 31, 1, 2
  ];

  const weekDays = ['L', 'M', 'X', 'J', 'V', 'S', 'D'];

  const filteredEvents = upcomingEvents.filter(event => {
    const matchesCategory = activeCategory === 'Todos' || event.category === activeCategory;
    const matchesSearch = event.title.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="events-container">
      <div className="events-header">
        <div className="header-title">
          <span className="header-icon">📅</span>
          <div>
            <h1>Eventos & Agenda</h1>
            <p>Organiza tu tiempo de forma inteligente con ayuda de Amigis.</p>
          </div>
        </div>
      </div>

      {/* Search and New Event */}
      <div className="search-section">
        <div className="search-bar">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder="Buscar evento…"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button className="new-event-btn">Nuevo Evento</button>
        </div>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        {stats.map((stat) => (
          <div key={stat.label} className="stat-card">
            <span className="stat-icon">{stat.icon}</span>
            <div className="stat-info">
              <span className="stat-value">{stat.value}</span>
              <span className="stat-label">{stat.label}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Amigis Agenda */}
      <div className="amigis-agenda-section">
        <div className="amigis-agenda-card">
          <div className="amigis-avatar">🦆</div>
          <div className="amigis-content">
            <h3>Agenda Inteligente de Amigis 🦆</h3>
            <p>"¡Hola! Revisé tu agenda y tienes un examen importante mañana. ¿Quieres que repasemos juntos durante 30 minutos? 📚"</p>
          </div>
        </div>
      </div>

      {/* Calendar */}
      <div className="calendar-section">
        <div className="calendar-header">
          <button className="nav-btn">‹</button>
          <h3>{currentMonth}</h3>
          <button className="nav-btn">›</button>
        </div>
        <div className="calendar-grid">
          {weekDays.map((day) => (
            <div key={day} className="calendar-day-header">{day}</div>
          ))}
          {calendarDays.map((day, index) => (
            <div 
              key={index} 
              className={`calendar-day ${day === 25 || day === 26 || day === 30 ? 'has-event' : ''}`}
            >
              {day}
            </div>
          ))}
        </div>
      </div>

      {/* Categories */}
      <div className="categories-section">
        <div className="categories">
          {categories.map((category) => (
            <button
              key={category.id}
              className={`category-btn ${activeCategory === category.id ? 'active' : ''}`}
              onClick={() => setActiveCategory(category.id)}
            >
              {category.icon} {category.name}
            </button>
          ))}
        </div>
      </div>

      {/* Upcoming Events */}
      <div className="events-section">
        <div className="section-header">
          <h3>Próximos Eventos</h3>
        </div>
        <div className="events-list">
          {filteredEvents.map((event) => (
            <div key={event.id} className="event-card">
              <span className="event-icon">{event.icon}</span>
              <div className="event-info">
                <h4>{event.title}</h4>
                <div className="event-meta">
                  <span>🕒 {event.date} · {event.time}</span>
                  <span>📍 {event.location}</span>
                </div>
              </div>
              <div className="event-actions">
                <button className="event-action-btn">✓</button>
                <button className="event-action-btn">🗑</button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Active Reminders */}
      <div className="reminders-section">
        <div className="section-header">
          <h3>Recordatorios Activos</h3>
        </div>
        <div className="reminders-list">
          {activeReminders.map((reminder) => (
            <div key={reminder.id} className="reminder-card">
              <span className="reminder-icon">{reminder.icon}</span>
              <div className="reminder-info">
                <h4>{reminder.title}</h4>
                <span className="reminder-time">{reminder.date} {reminder.time && `— ${reminder.time}`}</span>
              </div>
              <button className="reminder-action-btn">✓</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Events;
