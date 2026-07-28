import React from 'react';
import './Profile.css';

interface Badge {
  id: number;
  name: string;
  icon: string;
  description: string;
}

interface Milestone {
  id: number;
  icon: string;
  title: string;
}

const Profile: React.FC = () => {
  const badges: Badge[] = [
    { id: 1, name: 'Desarrollador', icon: '🥇', description: 'Completaste 10 cursos de código' },
    { id: 2, name: 'Estudiante Constante', icon: '🎓', description: 'Estudiaste 5 días seguidos' },
    { id: 3, name: 'Racha de 30 Días', icon: '🔥', description: 'Uso ininterrumpido de la app' },
    { id: 4, name: 'Amante de la Música', icon: '🎵', description: 'Escuchaste 50+ canciones' },
    { id: 5, name: 'Políglota', icon: '🌎', description: 'Tradujiste en más de 5 idiomas' },
    { id: 6, name: 'Experto en IA', icon: '🤖', description: '100+ conversaciones con Amigis' },
  ];

  const milestones: Milestone[] = [
    { id: 1, icon: '🚀', title: 'Te uniste a MiniAmigixV — Comenzaste tu viaje de aprendizaje inteligente.' },
    { id: 2, icon: '🎓', title: 'Completaste tu primer curso — "HTML & CSS desde cero".' },
    { id: 3, icon: '🏅', title: 'Alcanzaste el Nivel 10 — Desbloqueaste nuevos accesorios para Amigis.' },
    { id: 4, icon: '🤖', title: 'Conversación N° 100 con Amigis — Aprendiste a crear APIs con Django.' },
    { id: 5, icon: '📚', title: 'Finalizaste tu Ruta de Aprendizaje — Ruta Web Developer completada al 100%.' },
  ];

  const quickAccess = [
    { icon: '⭐', label: 'Tutoriales' },
    { icon: '🎵', label: 'Música' },
    { icon: '📚', label: 'Cursos' },
    { icon: '💬', label: 'Chats IA' },
    { icon: '🎮', label: 'Juegos' },
    { icon: '📰', label: 'Artículos' },
  ];

  const todayActivities = [
    { icon: '✔', text: 'Terminaste el tutorial Python desde cero' },
    { icon: '✔', text: 'Jugaste Sudoku en la Sala Arcade' },
    { icon: '✔', text: 'Escuchaste Lo-Fi Relax en Música' },
    { icon: '✔', text: 'Conversaste con Amigis IA' },
  ];

  const myFiles = [
    { icon: '📄', name: 'Documentos PDF', count: '14 archivos' },
    { icon: '📝', name: 'Apuntes & Notas', count: '32 notas' },
    { icon: '📷', name: 'Imágenes', count: '8 fotos' },
    { icon: '🎵', name: 'Audio & Música', count: '24 canciones' },
  ];

  return (
    <div className="profile-container">
      <div className="profile-header">
        <div className="header-title">
          <span className="header-icon">👤</span>
          <div>
            <h1>Mi Perfil</h1>
            <p>Administra tu cuenta, tus logros y tu progreso en MiniAmigixV.</p>
          </div>
        </div>
        <div className="header-actions">
          <button className="action-btn primary">✏️ Editar Perfil</button>
          <button className="action-btn secondary">📤 Compartir</button>
          <button className="action-btn secondary">⚙️ Configuración</button>
          <button className="action-btn secondary">📄 Reporte PDF</button>
        </div>
      </div>

      {/* User Profile */}
      <div className="user-profile-section">
        <div className="user-card">
          <div className="user-avatar">M</div>
          <div className="user-info">
            <h2>mariajosetacoc2005</h2>
            <p className="user-bio">💜 Desarrolladora de Software</p>
            <div className="user-details">
              <span>📧 mariajosetacoc2005@gmail.com</span>
              <span>•</span>
              <span>📍 Ecuador</span>
              <span>•</span>
              <span>🗓️ Unida en julio 2026</span>
            </div>
          </div>
        </div>
      </div>

      {/* Level & Streak */}
      <div className="level-streak-section">
        <div className="level-card">
          <span className="level-icon">⭐</span>
          <div className="level-info">
            <span className="level-number">Nivel 35</span>
            <span className="level-title">Desarrollador Avanzado</span>
          </div>
        </div>
        <div className="streak-card">
          <span className="streak-icon">🔥</span>
          <div className="streak-info">
            <span className="streak-number">18 Días</span>
            <span className="streak-label">Racha Activa</span>
          </div>
        </div>
      </div>

      {/* XP Progress */}
      <div className="xp-section">
        <h3>📈 Progreso a Nivel 36</h3>
        <div className="xp-progress">
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: '70%' }}></div>
          </div>
          <span className="xp-text">3,500 / 5,000 XP</span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid">
        <div className="stat-card">
          <span className="stat-icon">💬</span>
          <div className="stat-info">
            <span className="stat-value">124</span>
            <span className="stat-label">Chats IA</span>
          </div>
        </div>
        <div className="stat-card">
          <span className="stat-icon">📚</span>
          <div className="stat-info">
            <span className="stat-value">12</span>
            <span className="stat-label">Cursos</span>
          </div>
        </div>
        <div className="stat-card">
          <span className="stat-icon">🎓</span>
          <div className="stat-info">
            <span className="stat-value">28</span>
            <span className="stat-label">Tutoriales</span>
          </div>
        </div>
        <div className="stat-card">
          <span className="stat-icon">🎮</span>
          <div className="stat-info">
            <span className="stat-value">45</span>
            <span className="stat-label">Juegos</span>
          </div>
        </div>
        <div className="stat-card">
          <span className="stat-icon">🎵</span>
          <div className="stat-info">
            <span className="stat-value">36h</span>
            <span className="stat-label">Música</span>
          </div>
        </div>
        <div className="stat-card">
          <span className="stat-icon">🌎</span>
          <div className="stat-info">
            <span className="stat-value">89</span>
            <span className="stat-label">Traducciones</span>
          </div>
        </div>
        <div className="stat-card">
          <span className="stat-icon">🏆</span>
          <div className="stat-info">
            <span className="stat-value">16</span>
            <span className="stat-label">Logros</span>
          </div>
        </div>
      </div>

      {/* Badges */}
      <div className="badges-section">
        <div className="section-header">
          <h3>Insignias Desbloqueadas</h3>
        </div>
        <div className="badges-grid">
          {badges.map((badge) => (
            <div key={badge.id} className="badge-card">
              <span className="badge-icon">{badge.icon}</span>
              <div className="badge-info">
                <h4>{badge.name}</h4>
                <p>{badge.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Access */}
      <div className="quick-access-section">
        <div className="section-header">
          <h3>Accesos Rápidos a Favoritos</h3>
        </div>
        <div className="quick-access-grid">
          {quickAccess.map((item, index) => (
            <div key={index} className="quick-access-card">
              <span className="quick-icon">{item.icon}</span>
              <span className="quick-label">{item.label}</span>
            </div>
          ))}
        </div>
      </div>

      {/* History Milestones */}
      <div className="milestones-section">
        <div className="section-header">
          <h3>Hitos de tu Historia</h3>
        </div>
        <div className="milestones-timeline">
          {milestones.map((milestone) => (
            <div key={milestone.id} className="milestone-item">
              <span className="milestone-icon">{milestone.icon}</span>
              <span className="milestone-text">{milestone.title}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Amigis Pet */}
      <div className="amigis-pet-section">
        <div className="amigis-pet-card">
          <div className="amigis-avatar">🦆</div>
          <div className="amigis-info">
            <h3>Amigis</h3>
            <span className="amigis-level">Amigis Nivel 12</span>
            <span className="amigis-mood">😊 Ánimo: ¡Súper Feliz!</span>
            <span className="amigis-accessories">👕 Gorra + Audífonos DJ + Mochila</span>
            <p className="amigis-message">💬 "¡Has avanzado mucho esta semana! Solo te faltan 1,500 XP para el Nivel 36. Sigue así."</p>
          </div>
        </div>
        <button className="action-btn primary">Personalizar Amigis</button>
      </div>

      {/* Today's Activity */}
      <div className="activity-section">
        <div className="section-header">
          <h3>Actividad de Hoy</h3>
        </div>
        <div className="activity-list">
          {todayActivities.map((activity, index) => (
            <div key={index} className="activity-item">
              <span className="activity-icon">{activity.icon}</span>
              <span className="activity-text">{activity.text}</span>
            </div>
          ))}
        </div>
      </div>

      {/* My Files */}
      <div className="files-section">
        <div className="section-header">
          <h3>Mis Archivos</h3>
        </div>
        <div className="files-grid">
          {myFiles.map((file, index) => (
            <div key={index} className="file-card">
              <span className="file-icon">{file.icon}</span>
              <div className="file-info">
                <h4>{file.name}</h4>
                <span className="file-count">{file.count}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Profile;
