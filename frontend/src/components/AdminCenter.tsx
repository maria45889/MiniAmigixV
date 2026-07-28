import React from 'react';
import './AdminCenter.css';

interface User {
  id: number;
  username: string;
  email: string;
  status: string;
}

const AdminCenter: React.FC = () => {
  const users: User[] = [
    { id: 1, username: 'miniamigixv', email: 'miniamigixv@gmail.com', status: 'Activo' },
    { id: 2, username: 'mariajosetacoc2005', email: 'mariajosetacoc2005@gmail.com', status: 'Activo' },
  ];

  const recentActivities = [
    { time: 'Hace 2 min', action: 'Nuevo usuario registrado' },
    { time: 'Hace 5 min', action: 'Evento creado' },
    { time: 'Hace 10 min', action: 'Nuevo ticket de soporte' },
  ];

  const quickActions = [
    { icon: '➕', label: 'Crear usuario' },
    { icon: '📧', label: 'Enviar correo' },
    { icon: '📢', label: 'Enviar anuncio' },
    { icon: '📊', label: 'Generar reporte' },
  ];

  return (
    <div className="admin-center-container">
      <div className="admin-header">
        <div className="header-title">
          <span className="header-icon">🛡</span>
          <div>
            <h1>Centro de Administración</h1>
            <p>Bienvenido, mariajosetacoc2005. Gestiona MiniAmigixV desde aquí.</p>
          </div>
        </div>
      </div>

      {/* Overview Stats */}
      <div className="overview-stats">
        <div className="stat-card">
          <span className="stat-icon">👥</span>
          <div className="stat-info">
            <span className="stat-value">2</span>
            <span className="stat-label">Usuarios</span>
          </div>
        </div>
        <div className="stat-card">
          <span className="stat-icon">💬</span>
          <div className="stat-info">
            <span className="stat-value">1</span>
            <span className="stat-label">Chats IA</span>
          </div>
        </div>
        <div className="stat-card">
          <span className="stat-icon">🎵</span>
          <div className="stat-info">
            <span className="stat-value">0</span>
            <span className="stat-label">Canciones</span>
          </div>
        </div>
        <div className="stat-card">
          <span className="stat-icon">📅</span>
          <div className="stat-info">
            <span className="stat-value">0</span>
            <span className="stat-label">Eventos</span>
          </div>
        </div>
        <div className="stat-card">
          <span className="stat-icon">🎫</span>
          <div className="stat-info">
            <span className="stat-value">0</span>
            <span className="stat-label">Tickets</span>
          </div>
        </div>
      </div>

      {/* Entertainment Stats */}
      <div className="section">
        <div className="section-header">
          <h2>🎮 Entretenimiento</h2>
        </div>
        <div className="stats-grid">
          <div className="mini-stat">
            <span className="mini-stat-value">0</span>
            <span className="mini-stat-label">Canciones</span>
          </div>
          <div className="mini-stat">
            <span className="mini-stat-value">0</span>
            <span className="mini-stat-label">Playlists</span>
          </div>
          <div className="mini-stat">
            <span className="mini-stat-value">0</span>
            <span className="mini-stat-label">Favoritos</span>
          </div>
          <div className="mini-stat">
            <span className="mini-stat-value">0</span>
            <span className="mini-stat-label">Juegos</span>
          </div>
          <div className="mini-stat">
            <span className="mini-stat-value">0</span>
            <span className="mini-stat-label">Puntuaciones</span>
          </div>
          <div className="mini-stat">
            <span className="mini-stat-value">0</span>
            <span className="mini-stat-label">Logros</span>
          </div>
        </div>
      </div>

      {/* Study Stats */}
      <div className="section">
        <div className="section-header">
          <h2>📚 Estudio</h2>
        </div>
        <div className="stats-grid">
          <div className="mini-stat">
            <span className="mini-stat-value">0</span>
            <span className="mini-stat-label">Recursos</span>
          </div>
          <div className="mini-stat">
            <span className="mini-stat-value">0</span>
            <span className="mini-stat-label">Sesiones</span>
          </div>
          <div className="mini-stat">
            <span className="mini-stat-value">0</span>
            <span className="mini-stat-label">Pomodoros</span>
          </div>
        </div>
        <div className="empty-state">
          <p>No hay recursos</p>
        </div>
      </div>

      {/* Entertainment Modules */}
      <div className="section">
        <div className="section-header">
          <h2>🔗 Módulos de Entretenimiento</h2>
        </div>
        <div className="modules-grid">
          <div className="module-card">🎵 Música</div>
          <div className="module-card">🎮 Juegos</div>
          <div className="module-card">💬 Chat IA</div>
          <div className="module-card">🌤️ Clima</div>
          <div className="module-card">🌐 Traductor</div>
          <div className="module-card">⏰ Reloj</div>
        </div>
      </div>

      {/* Climate & Translation */}
      <div className="section">
        <div className="section-header">
          <h2>🌤️ Clima</h2>
        </div>
        <div className="stats-grid">
          <div className="mini-stat">
            <span className="mini-stat-value">6</span>
            <span className="mini-stat-label">Consultas de clima</span>
          </div>
        </div>
      </div>

      <div className="section">
        <div className="section-header">
          <h2>🌐 Traductor</h2>
        </div>
        <div className="stats-grid">
          <div className="mini-stat">
            <span className="mini-stat-value">0</span>
            <span className="mini-stat-label">Traducciones</span>
          </div>
        </div>
      </div>

      {/* Notifications */}
      <div className="section">
        <div className="section-header">
          <h2>🔔 Notificaciones</h2>
        </div>
        <div className="stats-grid">
          <div className="mini-stat">
            <span className="mini-stat-value">0</span>
            <span className="mini-stat-label">Sin leer</span>
          </div>
        </div>
        <div className="empty-state">
          <p>No hay notificaciones</p>
        </div>
      </div>

      {/* User Management */}
      <div className="section">
        <div className="section-header">
          <h2>👥 Gestión de Usuarios</h2>
        </div>
        <div className="table-container">
          <table className="users-table">
            <thead>
              <tr>
                <th>Usuario</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>
                    <div className="user-cell">
                      <span className="user-avatar">M</span>
                      <div className="user-details">
                        <span className="user-name">{user.username}</span>
                        <span className="user-email">{user.email}</span>
                      </div>
                    </div>
                  </td>
                  <td>
                    <span className="status-badge active">{user.status}</span>
                  </td>
                  <td>
                    <button className="action-btn">✉️</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Blog Management */}
      <div className="section">
        <div className="section-header">
          <h2>📝 Gestión del Blog</h2>
        </div>
        <div className="stats-grid">
          <div className="mini-stat">
            <span className="mini-stat-value">0</span>
            <span className="mini-stat-label">Publicaciones</span>
          </div>
          <div className="mini-stat">
            <span className="mini-stat-value">0</span>
            <span className="mini-stat-label">Comentarios</span>
          </div>
        </div>
        <div className="empty-state">
          <p>No hay publicaciones</p>
        </div>
        <button className="action-btn primary">Ir al Blog</button>
      </div>

      {/* Visitors */}
      <div className="section">
        <div className="section-header">
          <h2>🌍 Visitantes</h2>
        </div>
        <div className="stats-grid">
          <div className="mini-stat">
            <span className="mini-stat-value">0</span>
            <span className="mini-stat-label">Hoy</span>
          </div>
          <div className="mini-stat">
            <span className="mini-stat-value">0</span>
            <span className="mini-stat-label">Esta semana</span>
          </div>
          <div className="mini-stat">
            <span className="mini-stat-value">0</span>
            <span className="mini-stat-label">Este mes</span>
          </div>
        </div>
      </div>

      {/* System Status */}
      <div className="section">
        <div className="section-header">
          <h2>⚙️ Estado del Sistema</h2>
        </div>
        <div className="system-status">
          <div className="status-item">
            <span className="status-label">Chat IA</span>
            <span className="status-indicator online">●</span>
          </div>
          <div className="status-item">
            <span className="status-label">Música</span>
            <span className="status-indicator online">●</span>
          </div>
          <div className="status-item">
            <span className="status-label">Eventos</span>
            <span className="status-indicator online">●</span>
          </div>
          <div className="status-item">
            <span className="status-label">Traductor</span>
            <span className="status-indicator online">●</span>
          </div>
          <div className="status-item">
            <span className="status-label">Clima</span>
            <span className="status-indicator online">●</span>
          </div>
          <div className="status-item">
            <span className="status-label">Servidor</span>
            <span className="status-indicator online">●</span>
          </div>
        </div>
      </div>

      {/* Support */}
      <div className="section">
        <div className="section-header">
          <h2>🎧 Soporte</h2>
        </div>
        <div className="stats-grid">
          <div className="mini-stat">
            <span className="mini-stat-value">0</span>
            <span className="mini-stat-label">Pendientes</span>
          </div>
          <div className="mini-stat">
            <span className="mini-stat-value">0</span>
            <span className="mini-stat-label">Resueltos</span>
          </div>
          <div className="mini-stat">
            <span className="mini-stat-value">N/A</span>
            <span className="mini-stat-label">Tiempo promedio</span>
          </div>
        </div>
        <button className="action-btn primary">Ver tickets</button>
      </div>

      {/* Suggestions */}
      <div className="section">
        <div className="section-header">
          <h2>💡 Sugerencias</h2>
        </div>
        <div className="empty-state">
          <p>No hay sugerencias</p>
        </div>
        <button className="action-btn secondary">Ver todas</button>
      </div>

      {/* Recent Activity */}
      <div className="section">
        <div className="section-header">
          <h2>📊 Actividad Reciente</h2>
        </div>
        <div className="activity-timeline">
          {recentActivities.map((activity, index) => (
            <div key={index} className="activity-item">
              <span className="activity-time">{activity.time}</span>
              <span className="activity-action">{activity.action}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="section">
        <div className="section-header">
          <h2>⚡ Acciones Rápidas</h2>
        </div>
        <div className="quick-actions-grid">
          {quickActions.map((action, index) => (
            <button key={index} className="quick-action-btn">
              <span className="action-icon">{action.icon}</span>
              <span className="action-label">{action.label}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AdminCenter;
