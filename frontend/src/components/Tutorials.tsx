import React, { useState } from 'react';
import './Tutorials.css';

interface Tutorial {
  id: number;
  title: string;
  icon: string;
  level: string;
  duration: string;
  progress: number;
  xp: number;
  completed?: boolean;
}

interface LearningPath {
  id: number;
  title: string;
  icon: string;
  topics: string;
  progress: number;
}

interface Badge {
  id: number;
  name: string;
  icon: string;
}

const Tutorials: React.FC = () => {
  const [activeCategory, setActiveCategory] = useState('Todos');
  const [searchQuery, setSearchQuery] = useState('');

  const categories = [
    { id: 'Todos', name: 'Todos', icon: '📌' },
    { id: 'programacion', name: 'Programación', icon: '💻' },
    { id: 'web', name: 'Desarrollo Web', icon: '🌐' },
    { id: 'apps', name: 'Aplicaciones', icon: '📱' },
    { id: 'ia', name: 'IA', icon: '🤖' },
    { id: 'design', name: 'Diseño UI/UX', icon: '🎨' },
    { id: 'database', name: 'Bases de Datos', icon: '🗄' },
    { id: 'security', name: 'Ciberseguridad', icon: '🔐' },
    { id: 'cloud', name: 'Cloud', icon: '☁' },
    { id: 'git', name: 'Git & GitHub', icon: '⚙' },
  ];

  const userStats = {
    level: 12,
    xp: 340,
    xpToNext: 1000,
    totalXP: 340,
    badges: 4,
    coursesCompleted: 3,
    hoursLearned: 18,
    streak: 7
  };

  const tutorials: Tutorial[] = [
    {
      id: 1,
      title: 'Python desde Cero — Guía Completa',
      icon: '🐍',
      level: 'Principiante',
      duration: '4h 30min',
      progress: 75,
      xp: 80
    },
    {
      id: 2,
      title: 'HTML5 & CSS3 Moderno',
      icon: '🌐',
      level: 'Principiante',
      duration: '3h',
      progress: 100,
      xp: 60,
      completed: true
    },
    {
      id: 3,
      title: 'JavaScript ES2024 — De 0 a Experto',
      icon: '⚡',
      level: 'Intermedio',
      duration: '5h',
      progress: 45,
      xp: 100
    },
    {
      id: 4,
      title: 'Machine Learning con Python',
      icon: '🤖',
      level: 'Avanzado',
      duration: '6h',
      progress: 0,
      xp: 200
    },
    {
      id: 5,
      title: 'SQL & Bases de Datos Relacionales',
      icon: '🗄',
      level: 'Principiante',
      duration: '2h',
      progress: 20,
      xp: 50
    },
    {
      id: 6,
      title: 'Git & GitHub — Control de Versiones',
      icon: '⚙',
      level: 'Principiante',
      duration: '1h 30min',
      progress: 60,
      xp: 40
    }
  ];

  const learningPaths: LearningPath[] = [
    {
      id: 1,
      title: 'Desarrollo Web',
      icon: '🌐',
      topics: 'HTML · CSS · JS · Django',
      progress: 80
    },
    {
      id: 2,
      title: 'Desarrollo Móvil',
      icon: '📱',
      topics: 'Kotlin · Android · Firebase',
      progress: 15
    },
    {
      id: 3,
      title: 'Inteligencia Artificial',
      icon: '🤖',
      topics: 'Python · ML · IA Generativa',
      progress: 0
    },
    {
      id: 4,
      title: 'DevOps',
      icon: '🚀',
      topics: 'Git · Docker · Linux',
      progress: 30
    },
    {
      id: 5,
      title: 'Backend & Cloud',
      icon: '☁',
      topics: 'DRF · Node.js · PostgreSQL',
      progress: 50
    }
  ];

  const levelSystem = [
    { name: 'Explorador', level: 1, icon: '🥉' },
    { name: 'Aprendiz', level: '10-24', icon: '🥈', current: true },
    { name: 'Desarrollador', level: 25, icon: '🥇' },
    { name: 'Experto', level: 50, icon: '💎' },
    { name: 'Maestro MiniAmigixV', level: 100, icon: '👑' },
  ];

  const badges: Badge[] = [
    { id: 1, name: 'Web Dev', icon: '🌐' },
    { id: 2, name: 'Pythonista', icon: '🐍' },
    { id: 3, name: 'Git Pro', icon: '⚙' },
    { id: 4, name: 'Racha 7d', icon: '🔥' },
    { id: 5, name: 'ML Nerd', icon: '🤖' },
    { id: 6, name: 'Experto', icon: '💎' },
    { id: 7, name: 'Cloud', icon: '☁' },
    { id: 8, name: 'Maestro', icon: '👑' },
  ];

  const filteredTutorials = tutorials.filter(tutorial => {
    const matchesCategory = activeCategory === 'Todos';
    const matchesSearch = tutorial.title.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="tutorials-container">
      <div className="tutorials-header">
        <div className="header-title">
          <span className="header-icon">🎓</span>
          <div>
            <h1>Academia de Tutoriales</h1>
            <p>Aprende paso a paso con guías, código en vivo y retos de Amigis.</p>
          </div>
        </div>
      </div>

      {/* Search and Navigation */}
      <div className="search-section">
        <div className="search-bar">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder="Buscar tutorial…"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <div className="nav-buttons">
            <button className="nav-btn">Rutas</button>
            <button className="nav-btn">Insignias</button>
          </div>
        </div>
      </div>

      {/* User Stats */}
      <div className="stats-section">
        <div className="level-badge">
          <span className="badge-icon">🥈</span>
          <div className="level-info">
            <span className="level-name">Aprendiz</span>
            <span className="level-number">Nivel {userStats.level}</span>
          </div>
        </div>
        <div className="xp-progress">
          <span className="xp-text">{userStats.xp} / {userStats.xpToNext} XP para el siguiente nivel</span>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${(userStats.xp / userStats.xpToNext) * 100}%` }}></div>
          </div>
        </div>
        <div className="stats-grid">
          <div className="stat-item">
            <span className="stat-icon">340</span>
            <span className="stat-label">XP Total</span>
          </div>
          <div className="stat-item">
            <span className="stat-icon">4</span>
            <span className="stat-label">Insignias</span>
          </div>
          <div className="stat-item">
            <span className="stat-icon">3</span>
            <span className="stat-label">Cursos terminados</span>
          </div>
          <div className="stat-item">
            <span className="stat-icon">18h</span>
            <span className="stat-label">Horas aprendidas</span>
          </div>
          <div className="stat-item">
            <span className="stat-icon">7</span>
            <span className="stat-label">Racha de estudio</span>
          </div>
          <div className="stat-item">
            <span className="stat-icon">📈</span>
            <span className="stat-label">Nv.{userStats.level}</span>
          </div>
        </div>
      </div>

      {/* Amigis Tutor */}
      <div className="amigis-tutor-section">
        <div className="amigis-tutor-card">
          <div className="amigis-avatar">🦆</div>
          <div className="amigis-content">
            <h3>Amigis Tutor 🦆</h3>
            <p>"¡Hola! ¿Lista para aprender algo nuevo hoy? Tengo un reto de Python que creo que te va a encantar. ¿Comenzamos? 🚀"</p>
            <button className="challenge-btn">🧩 Ver Reto</button>
          </div>
        </div>
      </div>

      {/* Featured Tutorial */}
      <div className="featured-section">
        <div className="featured-card">
          <div className="featured-icon">🐍</div>
          <div className="featured-content">
            <span className="featured-badge">🌟 DESTACADO DEL DÍA</span>
            <h3>Aprende Django desde Cero — Backend Completo</h3>
            <div className="featured-meta">
              <span>⏱ 3 horas</span>
              <span>•</span>
              <span>⭐ Principiante</span>
              <span>•</span>
              <span>💻 Python & Django</span>
              <span>•</span>
              <span>🔥 +150 XP</span>
            </div>
            <div className="featured-actions">
              <button className="action-btn primary">▶ Comenzar Tutorial</button>
              <button className="action-btn secondary">📖 Ver Contenido</button>
            </div>
          </div>
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

      {/* Tutorials List */}
      <div className="tutorials-section">
        <div className="section-header">
          <h3>Tutoriales</h3>
        </div>
        <div className="tutorials-list">
          {filteredTutorials.map((tutorial) => (
            <div key={tutorial.id} className="tutorial-card">
              <span className="tutorial-icon">{tutorial.icon}</span>
              <div className="tutorial-info">
                <h4>{tutorial.title}</h4>
                <div className="tutorial-meta">
                  <span>{tutorial.level}</span>
                  <span>⏱ {tutorial.duration}</span>
                </div>
                <div className="tutorial-progress">
                  <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${tutorial.progress}%` }}></div>
                  </div>
                  <span className="progress-text">{tutorial.progress}% completado · +{tutorial.xp} XP</span>
                </div>
              </div>
              <div className="tutorial-actions">
                {tutorial.completed ? (
                  <button className="action-btn completed">🏅 Ver Certificado</button>
                ) : tutorial.progress > 0 ? (
                  <button className="action-btn primary">▶ Continuar</button>
                ) : (
                  <button className="action-btn primary">▶ Comenzar</button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Learning Paths */}
      <div className="learning-paths-section">
        <div className="section-header">
          <h3>Rutas de Aprendizaje</h3>
        </div>
        <div className="learning-paths-grid">
          {learningPaths.map((path) => (
            <div key={path.id} className="path-card">
              <span className="path-icon">{path.icon}</span>
              <div className="path-info">
                <h4>{path.title}</h4>
                <p className="path-topics">{path.topics}</p>
                <div className="path-progress">
                  <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${path.progress}%` }}></div>
                  </div>
                  <span className="progress-text">{path.progress}%</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Level System */}
      <div className="level-system-section">
        <div className="section-header">
          <h3>Sistema de Niveles</h3>
        </div>
        <div className="level-system-grid">
          {levelSystem.map((level) => (
            <div key={level.name} className={`level-card ${level.current ? 'current' : ''}`}>
              <span className="level-badge-icon">{level.icon}</span>
              <div className="level-card-info">
                <h4>{level.name}</h4>
                <span className="level-range">Nivel {level.level}</span>
              </div>
              {level.current && <span className="current-indicator">← Tú estás aquí</span>}
            </div>
          ))}
        </div>
      </div>

      {/* Badges */}
      <div className="badges-section">
        <div className="section-header">
          <h3>Mis Insignias</h3>
        </div>
        <div className="badges-grid">
          {badges.map((badge) => (
            <div key={badge.id} className="badge-card">
              <span className="badge-icon">{badge.icon}</span>
              <span className="badge-name">{badge.name}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Tutorials;
