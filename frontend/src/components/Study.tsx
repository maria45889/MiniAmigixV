import React, { useState, useEffect } from 'react';
import './Study.css';

interface Course {
  id: number;
  title: string;
  description: string;
  progress: number;
  icon: string;
  completed?: boolean;
}

interface Note {
  id: number;
  title: string;
  date: string;
  content: string;
}

interface Accessory {
  id: number;
  name: string;
  icon: string;
  price: number;
  unlocked: boolean;
  equipped?: boolean;
}

const Study: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'courses' | 'pomodoro' | 'notes' | 'academy'>('courses');
  const [pomodoroTime, setPomodoroTime] = useState(25 * 60);
  const [isRunning, setIsRunning] = useState(false);
  const [completedPomodoros, setCompletedPomodoros] = useState(4);
  const [dailyGoals, setDailyGoals] = useState([
    { id: 1, text: 'Estudiar 2 horas de programación', completed: false },
    { id: 2, text: 'Completar un módulo de curso', completed: false },
    { id: 3, text: 'Leer 20 páginas de documentación', completed: false },
    { id: 4, text: 'Resolver 5 ejercicios prácticos', completed: false },
  ]);

  const courses: Course[] = [
    { id: 1, title: 'Desarrollo de Software', description: 'Arquitectura, patrones y código limpio.', progress: 80, icon: '💻' },
    { id: 2, title: 'HTML5 y CSS3', description: 'Maquetación web y Glassmorphism.', progress: 100, icon: '🌐', completed: true },
    { id: 3, title: 'JavaScript Moderno', description: 'ES6+, Promesas y Async/Await.', progress: 60, icon: '⚙️' },
    { id: 4, title: 'Python Avanzado', description: 'Django, APIs y Data Science.', progress: 45, icon: '🐍' },
    { id: 5, title: 'Java & Spring Boot', description: 'POO, Servlets y Microservicios.', progress: 90, icon: '☕' },
    { id: 6, title: 'Bases de Datos SQL & NoSQL', description: 'PostgreSQL, SQLite y MongoDB.', progress: 70, icon: '🗄️' },
    { id: 7, title: 'Matemáticas Avanzadas', description: 'Cálculo, álgebra lineal y estadística.', progress: 55, icon: '📐' },
    { id: 8, title: 'Derecho y Legislación', description: 'Derecho civil, penal y corporativo.', progress: 30, icon: '⚖️' },
    { id: 9, title: 'Inglés Profesional', description: 'Gramática, conversación y negocios.', progress: 85, icon: '🌍' },
    { id: 10, title: 'Negocios y Emprendimiento', description: 'Marketing, finanzas y gestión.', progress: 40, icon: '📊' },
    { id: 11, title: 'Arte y Diseño Digital', description: 'Illustrator, Photoshop y UX/UI.', progress: 65, icon: '🎨' },
    { id: 12, title: 'Ciencias Naturales', description: 'Biología, química y física.', progress: 50, icon: '🔬' },
    { id: 13, title: 'Historia Universal', description: 'Civilizaciones antiguas y modernas.', progress: 75, icon: '🏛️' },
    { id: 14, title: 'Medicina y Salud', description: 'Anatomía, fisiología y primeros auxilios.', progress: 35, icon: '🏥' },
    { id: 15, title: 'Matemáticas Básicas', description: 'Suma, resta, multiplicación y división.', progress: 60, icon: '📊' },
  ];

  const notes: Note[] = [
    { id: 1, title: 'Apuntes de Django APIs', date: 'Hoy', content: 'Conceptos clave: Serializers, ViewSets, Routers y autenticación por Token.' },
    { id: 2, title: 'Comandos Git Esenciales', date: 'Ayer', content: 'git checkout -b feature, git commit -m, git push origin branch.' },
    { id: 3, title: 'Trucos CSS Glassmorphism', date: 'Hace 3 días', content: 'backdrop-filter: blur(20px), background: rgba(255,255,255,0.08), border translucido.' },
  ];

  const accessories: Accessory[] = [
    { id: 1, name: 'Gorra Gamer', icon: '🧢', price: 0, unlocked: true, equipped: false },
    { id: 2, name: 'Gafas Neón', icon: '👓', price: 0, unlocked: true, equipped: false },
    { id: 3, name: 'Mochila de Estudio', icon: '🎒', price: 100, unlocked: false },
    { id: 4, name: 'Laptop Neón', icon: '💻', price: 0, unlocked: true, equipped: true },
  ];

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isRunning && pomodoroTime > 0) {
      interval = setInterval(() => {
        setPomodoroTime(prev => prev - 1);
      }, 1000);
    } else if (pomodoroTime === 0) {
      setIsRunning(false);
      setCompletedPomodoros(prev => prev + 1);
    }
    return () => clearInterval(interval);
  }, [isRunning, pomodoroTime]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const toggleGoal = (id: number) => {
    setDailyGoals(goals => goals.map(goal => 
      goal.id === id ? { ...goal, completed: !goal.completed } : goal
    ));
  };

  const buyAccessory = (accessory: Accessory) => {
    if (!accessory.unlocked && 320 >= accessory.price) {
      // In a real app, this would update the user's coins
      alert(`¡Comprado ${accessory.name}!`);
    }
  };

  return (
    <div className="study-container">
      <div className="study-header">
        <div className="study-title">
          <span className="study-icon">📚</span>
          <div>
            <h1>Estudio & Aprendizaje</h1>
            <p>Aprende a tu ritmo con la guía inteligente de MiniAmigixV y Amigis.</p>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="study-stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📚</div>
          <div className="stat-value">28.5h</div>
          <div className="stat-label">Horas Estudiadas</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🔥</div>
          <div className="stat-value">7 días</div>
          <div className="stat-label">Racha Diaria</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🏆</div>
          <div className="stat-value">4</div>
          <div className="stat-label">Cursos Terminados</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">⭐</div>
          <div className="stat-value">Avanzado</div>
          <div className="stat-label">Nivel de Aprendizaje</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">📈</div>
          <div className="stat-value">+12%</div>
          <div className="stat-label">Progreso Semanal</div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="study-tabs">
        <button 
          className={`tab-btn ${activeTab === 'courses' ? 'active' : ''}`}
          onClick={() => setActiveTab('courses')}
        >
          📖 Mis Cursos
        </button>
        <button 
          className={`tab-btn ${activeTab === 'pomodoro' ? 'active' : ''}`}
          onClick={() => setActiveTab('pomodoro')}
        >
          ⏱️ Pomodoro
        </button>
        <button 
          className={`tab-btn ${activeTab === 'notes' ? 'active' : ''}`}
          onClick={() => setActiveTab('notes')}
        >
          📝 Mis Apuntes
        </button>
        <button 
          className={`tab-btn ${activeTab === 'academy' ? 'active' : ''}`}
          onClick={() => setActiveTab('academy')}
        >
          🎓 Academia
        </button>
      </div>

      {/* Content Sections */}
      {activeTab === 'courses' && (
        <div className="courses-section">
          <h2 className="section-title">📖 Mis Cursos ({courses.length} Total)</h2>
          <div className="courses-grid">
            {courses.map(course => (
              <div key={course.id} className="course-card">
                <div className="course-icon">{course.icon}</div>
                <div className="course-info">
                  <h3>{course.title}</h3>
                  <p>{course.description}</p>
                  <div className="course-progress">
                    <div className="progress-bar">
                      <div 
                        className="progress-fill" 
                        style={{ width: `${course.progress}%` }}
                      ></div>
                    </div>
                    <span className="progress-text">{course.progress}%</span>
                  </div>
                </div>
                <button className="course-btn">
                  {course.completed ? 'Repasar Contenido' : 'Continuar Curso'}
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'pomodoro' && (
        <div className="pomodoro-section">
          <div className="pomodoro-timer">
            <h2>Temporizador Pomodoro</h2>
            <div className="timer-display">{formatTime(pomodoroTime)}</div>
            <div className="timer-controls">
              <button 
                className="timer-btn"
                onClick={() => setIsRunning(!isRunning)}
              >
                {isRunning ? '⏸ Pausar' : '▶ Iniciar'}
              </button>
              <button 
                className="timer-btn"
                onClick={() => {
                  setPomodoroTime(25 * 60);
                  setIsRunning(false);
                }}
              >
                🔄 Reiniciar
              </button>
            </div>
            <div className="pomodoro-stats">
              🍅 Pomodoros completados hoy: {completedPomodoros}
            </div>
          </div>

          <div className="daily-goals">
            <h3>Metas del Día</h3>
            {dailyGoals.map(goal => (
              <label key={goal.id} className="goal-item">
                <input 
                  type="checkbox" 
                  checked={goal.completed}
                  onChange={() => toggleGoal(goal.id)}
                />
                <span className={goal.completed ? 'completed' : ''}>{goal.text}</span>
              </label>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'notes' && (
        <div className="notes-section">
          <div className="notes-header">
            <h2>Mis Apuntes & Notas</h2>
            <div className="notes-actions">
              <button className="action-btn">Nueva Nota</button>
              <button className="action-btn">Exportar Apuntes</button>
            </div>
          </div>
          <div className="notes-list">
            {notes.map(note => (
              <div key={note.id} className="note-card">
                <div className="note-header">
                  <span className="note-pin">📌</span>
                  <span className="note-date">{note.date}</span>
                </div>
                <h3>{note.title}</h3>
                <p>{note.content}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'academy' && (
        <div className="academy-section">
          <div className="academy-header">
            <h2>🎓 Academia de Amigis & Tienda de Accesorios</h2>
            <div className="coins-display">
              🪙 320 Monedas Amigis
            </div>
          </div>
          <p className="academy-description">
            Cada curso completado te otorga insignias, experiencia XP y desbloquea accesorios exclusivos para vestir a tu mascota Amigis.
          </p>
          <div className="accessories-grid">
            {accessories.map(accessory => (
              <div key={accessory.id} className={`accessory-card ${accessory.unlocked ? 'unlocked' : 'locked'} ${accessory.equipped ? 'equipped' : ''}`}>
                <div className="accessory-icon">{accessory.icon}</div>
                <h4>{accessory.name}</h4>
                {accessory.unlocked ? (
                  <span className="status-badge">
                    {accessory.equipped ? 'Equipado ✔' : 'Desbloqueado ✔'}
                  </span>
                ) : (
                  <div className="price-tag">🪙 {accessory.price}</div>
                )}
                {!accessory.unlocked && (
                  <button 
                    className="buy-btn"
                    onClick={() => buyAccessory(accessory)}
                  >
                    Comprar
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Study;
