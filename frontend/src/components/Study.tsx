import React, { useState, useEffect } from 'react';
import './Study.css';

interface Note {
  id: number;
  title: string;
  date: string;
  content: string;
  category?: string;
}

interface Accessory {
  id: number;
  name: string;
  icon: string;
  price: number;
  unlocked: boolean;
  equipped?: boolean;
}

interface EducationalLevel {
  id: string;
  name: string;
  icon: string;
  description: string;
}

interface Subject {
  id: string;
  name: string;
  icon: string;
  category: string;
}

interface Activity {
  id: string;
  title: string;
  type: 'quiz' | 'flashcard' | 'matching' | 'complete' | 'experiment';
  subject: string;
  difficulty: 'easy' | 'medium' | 'hard';
  duration: number;
  xpReward: number;
  coinsReward: number;
}

interface DailyChallenge {
  id: string;
  title: string;
  description: string;
  xpReward: number;
  coinsReward: number;
  completed: boolean;
}

interface UserProgress {
  xp: number;
  coins: number;
  level: number;
  streak: number;
  hoursStudied: number;
  activitiesCompleted: number;
  badges: string[];
}

interface AccessibilitySettings {
  textSize: 'normal' | 'large' | 'extraLarge';
  highContrast: boolean;
  animationsEnabled: boolean;
  simplifiedNavigation: boolean;
  screenReaderEnabled: boolean;
}

const Study: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'home' | 'subjects' | 'activities' | 'pomodoro' | 'notes' | 'progress' | 'academy'>('home');
  const [selectedLevel, setSelectedLevel] = useState<string>('');
  const [selectedTime, setSelectedTime] = useState<string>('');
  const [pomodoroTime, setPomodoroTime] = useState(25 * 60);
  const [isRunning, setIsRunning] = useState(false);
  const [completedPomodoros, setCompletedPomodoros] = useState(4);
  const [userProgress, setUserProgress] = useState<UserProgress>({
    xp: 2850,
    coins: 320,
    level: 8,
    streak: 7,
    hoursStudied: 28.5,
    activitiesCompleted: 45,
    badges: ['🌟 Primeros Pasos', '🔥 Racha de 7 días', '📚 Aprendiz Dedicado']
  });
  const [accessibilitySettings, setAccessibilitySettings] = useState<AccessibilitySettings>({
    textSize: 'normal',
    highContrast: false,
    animationsEnabled: true,
    simplifiedNavigation: false,
    screenReaderEnabled: false
  });
  const [showAccessibilityPanel, setShowAccessibilityPanel] = useState(false);
  const [selectedAgeGroup, setSelectedAgeGroup] = useState<string>('');
  const [selectedLearningStyle, setSelectedLearningStyle] = useState<string>('');
  const [dailyGoals, setDailyGoals] = useState([
    { id: 1, text: 'Estudiar 2 horas de programación', completed: false },
    { id: 2, text: 'Completar un módulo de curso', completed: false },
    { id: 3, text: 'Leer 20 páginas de documentación', completed: false },
    { id: 4, text: 'Resolver 5 ejercicios prácticos', completed: false },
  ]);

  const educationalLevels: EducationalLevel[] = [
    { id: 'school', name: 'Escuela', icon: '🎒', description: 'Para niños de primaria' },
    { id: 'middle', name: 'Colegio', icon: '📖', description: 'Para estudiantes de secundaria' },
    { id: 'technical', name: 'Técnico', icon: '🔧', description: 'Bachillerato técnico' },
    { id: 'university', name: 'Universidad', icon: '🎓', description: 'Estudios superiores' },
    { id: 'professional', name: 'Profesional', icon: '💼', description: 'Formación continua' },
    { id: 'curiosity', name: 'Curiosidad', icon: '🌎', description: 'Aprender por placer' },
  ];

  const timeOptions = [
    { id: '5min', label: '5 min', value: 5 },
    { id: '15min', label: '15 min', value: 15 },
    { id: '30min', label: '30 min', value: 30 },
    { id: '1hour', label: '1 hora', value: 60 },
    { id: 'more', label: 'Más tiempo', value: 120 },
  ];

  const subjects: Subject[] = [
    { id: 'math', name: 'Matemáticas', icon: '📐', category: 'STEM' },
    { id: 'science', name: 'Ciencias', icon: '🔬', category: 'STEM' },
    { id: 'social', name: 'Estudios Sociales', icon: '🌎', category: 'Humanidades' },
    { id: 'language', name: 'Lengua y Literatura', icon: '📚', category: 'Humanidades' },
    { id: 'english', name: 'Idiomas', icon: '🇬🇧', category: 'Idiomas' },
    { id: 'tech', name: 'Tecnología', icon: '💻', category: 'STEM' },
    { id: 'art', name: 'Arte y Diseño', icon: '🎨', category: 'Artes' },
    { id: 'finance', name: 'Finanzas', icon: '💰', category: 'Negocios' },
    { id: 'psychology', name: 'Psicología', icon: '🧠', category: 'Ciencias' },
    { id: 'environment', name: 'Medio Ambiente', icon: '🌱', category: 'Ciencias' },
    { id: 'law', name: 'Derecho', icon: '⚖️', category: 'Humanidades' },
    { id: 'health', name: 'Salud', icon: '🏥', category: 'Ciencias' },
    { id: 'admin', name: 'Administración', icon: '📊', category: 'Negocios' },
    { id: 'electronics', name: 'Electrónica', icon: '🔧', category: 'STEM' },
    { id: 'mechanics', name: 'Mecánica', icon: '⚙️', category: 'STEM' },
    { id: 'cooking', name: 'Cocina', icon: '🍳', category: 'Artes' },
    { id: 'photography', name: 'Fotografía', icon: '📸', category: 'Artes' },
    { id: 'music', name: 'Música', icon: '🎵', category: 'Artes' },
    { id: 'communication', name: 'Comunicación', icon: '🗣️', category: 'Humanidades' },
    { id: 'culture', name: 'Cultura General', icon: '🌟', category: 'General' },
  ];

  const quickActivities: Activity[] = [
    { id: '1', title: '¿Por qué soñamos?', type: 'quiz', subject: 'Psicología', difficulty: 'easy', duration: 5, xpReward: 25, coinsReward: 10 },
    { id: '2', title: 'Organización del dinero', type: 'quiz', subject: 'Finanzas', difficulty: 'easy', duration: 5, xpReward: 25, coinsReward: 10 },
    { id: '3', title: 'Husos horarios explicados', type: 'flashcard', subject: 'Cultura General', difficulty: 'easy', duration: 5, xpReward: 20, coinsReward: 8 },
    { id: '4', title: 'Cambio de color químico', type: 'experiment', subject: 'Ciencias', difficulty: 'medium', duration: 5, xpReward: 30, coinsReward: 15 },
    { id: '5', title: 'Matemáticas en la vida real', type: 'quiz', subject: 'Matemáticas', difficulty: 'easy', duration: 5, xpReward: 25, coinsReward: 10 },
    { id: '6', title: '¿Qué es una API?', type: 'flashcard', subject: 'Tecnología', difficulty: 'medium', duration: 5, xpReward: 30, coinsReward: 15 },
    { id: '7', title: 'Teoría del color', type: 'quiz', subject: 'Arte', difficulty: 'easy', duration: 5, xpReward: 25, coinsReward: 10 },
    { id: '8', title: '5 palabras en inglés', type: 'flashcard', subject: 'Idiomas', difficulty: 'easy', duration: 5, xpReward: 20, coinsReward: 8 },
  ];

  const dailyChallenge: DailyChallenge = {
    id: 'today',
    title: 'Razonamiento Lógico',
    description: 'Resuelve este problema matemático en menos de 3 minutos',
    xpReward: 50,
    coinsReward: 20,
    completed: false,
  };


  const notes: Note[] = [
    { id: 1, title: 'Apuntes de Django APIs', date: 'Hoy', content: 'Conceptos clave: Serializers, ViewSets, Routers y autenticación por Token.', category: 'Tecnología' },
    { id: 2, title: 'Comandos Git Esenciales', date: 'Ayer', content: 'git checkout -b feature, git commit -m, git push origin branch.', category: 'Tecnología' },
    { id: 3, title: 'Trucos CSS Glassmorphism', date: 'Hace 3 días', content: 'backdrop-filter: blur(20px), background: rgba(255,255,255,0.08), border translucido.', category: 'Arte' },
    { id: 4, title: 'Fórmulas de Cálculo', date: 'Hace 5 días', content: 'Derivadas, integrales y límites básicos.', category: 'Matemáticas' },
    { id: 5, title: 'Vocabulario Inglés', date: 'Hace 1 semana', content: 'Palabras clave para negocios y presentaciones.', category: 'Idiomas' },
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
      completePomodoro();
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
    if (!dailyGoals.find(g => g.id === id)?.completed) {
      setUserProgress(prev => ({ ...prev, xp: prev.xp + 10, coins: prev.coins + 5 }));
    }
  };

  const completePomodoro = () => {
    setUserProgress(prev => ({
      ...prev,
      xp: prev.xp + 25,
      coins: prev.coins + 10,
      hoursStudied: prev.hoursStudied + 0.42
    }));
  };

  const completeActivity = (activity: Activity) => {
    setUserProgress(prev => ({
      ...prev,
      xp: prev.xp + activity.xpReward,
      coins: prev.coins + activity.coinsReward,
      activitiesCompleted: prev.activitiesCompleted + 1
    }));
  };

  const completeDailyChallenge = () => {
    setUserProgress(prev => ({
      ...prev,
      xp: prev.xp + dailyChallenge.xpReward,
      coins: prev.coins + dailyChallenge.coinsReward,
      streak: prev.streak + 1
    }));
  };

  const selectLevel = (levelId: string) => {
    setSelectedLevel(levelId);
    setActiveTab('subjects');
  };

  const selectTime = (timeId: string) => {
    setSelectedTime(timeId);
  };

  const getLevelForXP = (xp: number) => {
    return Math.floor(xp / 350) + 1;
  };


  const getProgressToNextLevel = (xp: number) => {
    const currentLevel = getLevelForXP(xp);
    const xpForCurrentLevel = (currentLevel - 1) * 350;
    const xpForNextLevel = currentLevel * 350;
    return ((xp - xpForCurrentLevel) / (xpForNextLevel - xpForCurrentLevel)) * 100;
  };

  const buyAccessory = (accessory: Accessory) => {
    if (!accessory.unlocked && userProgress.coins >= accessory.price) {
      setUserProgress(prev => ({ ...prev, coins: prev.coins - accessory.price }));
      alert(`¡Comprado ${accessory.name}!`);
    }
  };

  const updateAccessibilitySetting = <K extends keyof AccessibilitySettings>(
    key: K,
    value: AccessibilitySettings[K]
  ) => {
    setAccessibilitySettings(prev => ({ ...prev, [key]: value }));
  };

  const getTextSizeClass = () => {
    switch (accessibilitySettings.textSize) {
      case 'large': return 'text-large';
      case 'extraLarge': return 'text-extra-large';
      default: return 'text-normal';
    }
  };

  const getContrastClass = () => {
    return accessibilitySettings.highContrast ? 'high-contrast' : '';
  };

  const getAnimationClass = () => {
    return accessibilitySettings.animationsEnabled ? '' : 'animations-reduced';
  };

  const ageGroups = [
    { id: '6-9', name: '6–9 años', icon: '🧒' },
    { id: '10-12', name: '10–12 años', icon: '👦' },
    { id: '13-15', name: '13–15 años', icon: '🎒' },
    { id: '16-18', name: '16–18 años', icon: '🔧' },
    { id: '18+', name: '18+ años', icon: '🎓' },
  ];

  const learningStyles = [
    { id: 'visual', name: 'Visual', icon: '👁️' },
    { id: 'auditory', name: 'Auditivo', icon: '👂' },
    { id: 'kinesthetic', name: 'Kinestésico', icon: '🖐️' },
    { id: 'reading', name: 'Lectura/Escritura', icon: '📖' },
  ];

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Escape to close accessibility panel
      if (e.key === 'Escape' && showAccessibilityPanel) {
        setShowAccessibilityPanel(false);
      }
      
      // Tab navigation enhancement
      if (e.key === 'Tab') {
        const focusableElements = document.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        const firstElement = focusableElements[0] as HTMLElement;
        const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;
        
        if (e.shiftKey && document.activeElement === firstElement) {
          e.preventDefault();
          lastElement.focus();
        } else if (!e.shiftKey && document.activeElement === lastElement) {
          e.preventDefault();
          firstElement.focus();
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [showAccessibilityPanel]);

  return (
    <div className={`study-container ${getTextSizeClass()} ${getContrastClass()} ${getAnimationClass()}`}>
      <div className="study-header">
        <div className="study-title">
          <span className="study-icon">📚</span>
          <div>
            <h1>Estudio & Aprendizaje</h1>
            <p>Aprende a tu ritmo con la guía inteligente de MiniAmigixV y Amigis.</p>
          </div>
        </div>
        <div className="user-level-badge">
          <span className="level-number">Nivel {userProgress.level}</span>
          <span className="level-title">Explorador del Conocimiento</span>
          <div className="level-progress">
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${getProgressToNextLevel(userProgress.xp)}%` }}></div>
            </div>
            <span className="progress-text">{getProgressToNextLevel(userProgress.xp).toFixed(0)}%</span>
          </div>
        </div>
        <button 
          className="accessibility-toggle-btn"
          onClick={() => setShowAccessibilityPanel(!showAccessibilityPanel)}
          aria-label="Abrir configuración de accesibilidad"
          title="Accesibilidad"
        >
          ⚙️ Accesibilidad
        </button>
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
          className={`tab-btn ${activeTab === 'home' ? 'active' : ''}`}
          onClick={() => setActiveTab('home')}
        >
          🏠 Inicio
        </button>
        <button 
          className={`tab-btn ${activeTab === 'subjects' ? 'active' : ''}`}
          onClick={() => setActiveTab('subjects')}
        >
          📚 Materias
        </button>
        <button 
          className={`tab-btn ${activeTab === 'activities' ? 'active' : ''}`}
          onClick={() => setActiveTab('activities')}
        >
          🎮 Actividades
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
          📝 Apuntes
        </button>
        <button 
          className={`tab-btn ${activeTab === 'progress' ? 'active' : ''}`}
          onClick={() => setActiveTab('progress')}
        >
          📊 Progreso
        </button>
        <button 
          className={`tab-btn ${activeTab === 'academy' ? 'active' : ''}`}
          onClick={() => setActiveTab('academy')}
        >
          🎓 Academia
        </button>
      </div>

      {/* Accessibility Panel */}
      {showAccessibilityPanel && (
        <div className="accessibility-panel" role="dialog" aria-modal="true" aria-labelledby="accessibility-title">
          <div className="accessibility-panel-header">
            <h3 id="accessibility-title">⚙️ Accesibilidad</h3>
            <button 
              className="accessibility-close-btn"
              onClick={() => setShowAccessibilityPanel(false)}
              aria-label="Cerrar panel de accesibilidad"
            >
              ✕
            </button>
          </div>
          
          <div className="accessibility-section">
            <h4>🔤 Tamaño del texto</h4>
            <div className="accessibility-options">
              <button 
                className={`accessibility-option ${accessibilitySettings.textSize === 'normal' ? 'active' : ''}`}
                onClick={() => updateAccessibilitySetting('textSize', 'normal')}
                aria-pressed={accessibilitySettings.textSize === 'normal'}
              >
                Normal
              </button>
              <button 
                className={`accessibility-option ${accessibilitySettings.textSize === 'large' ? 'active' : ''}`}
                onClick={() => updateAccessibilitySetting('textSize', 'large')}
                aria-pressed={accessibilitySettings.textSize === 'large'}
              >
                Grande
              </button>
              <button 
                className={`accessibility-option ${accessibilitySettings.textSize === 'extraLarge' ? 'active' : ''}`}
                onClick={() => updateAccessibilitySetting('textSize', 'extraLarge')}
                aria-pressed={accessibilitySettings.textSize === 'extraLarge'}
              >
                Muy grande
              </button>
            </div>
          </div>

          <div className="accessibility-section">
            <h4>🎨 Contraste</h4>
            <div className="accessibility-options">
              <button 
                className={`accessibility-option ${!accessibilitySettings.highContrast ? 'active' : ''}`}
                onClick={() => updateAccessibilitySetting('highContrast', false)}
                aria-pressed={!accessibilitySettings.highContrast}
              >
                Normal
              </button>
              <button 
                className={`accessibility-option ${accessibilitySettings.highContrast ? 'active' : ''}`}
                onClick={() => updateAccessibilitySetting('highContrast', true)}
                aria-pressed={accessibilitySettings.highContrast}
              >
                Alto contraste
              </button>
            </div>
          </div>

          <div className="accessibility-section">
            <h4>✨ Animaciones</h4>
            <div className="accessibility-options">
              <button 
                className={`accessibility-option ${accessibilitySettings.animationsEnabled ? 'active' : ''}`}
                onClick={() => updateAccessibilitySetting('animationsEnabled', true)}
                aria-pressed={accessibilitySettings.animationsEnabled}
              >
                Activadas
              </button>
              <button 
                className={`accessibility-option ${!accessibilitySettings.animationsEnabled ? 'active' : ''}`}
                onClick={() => updateAccessibilitySetting('animationsEnabled', false)}
                aria-pressed={!accessibilitySettings.animationsEnabled}
              >
                Reducidas
              </button>
            </div>
          </div>

          <div className="accessibility-section">
            <h4>🧭 Navegación simplificada</h4>
            <div className="accessibility-options">
              <button 
                className={`accessibility-option ${!accessibilitySettings.simplifiedNavigation ? 'active' : ''}`}
                onClick={() => updateAccessibilitySetting('simplifiedNavigation', false)}
                aria-pressed={!accessibilitySettings.simplifiedNavigation}
              >
                Normal
              </button>
              <button 
                className={`accessibility-option ${accessibilitySettings.simplifiedNavigation ? 'active' : ''}`}
                onClick={() => updateAccessibilitySetting('simplifiedNavigation', true)}
                aria-pressed={accessibilitySettings.simplifiedNavigation}
              >
                Simplificada
              </button>
            </div>
          </div>

          <div className="accessibility-section">
            <h4>🔊 Lectura de contenido</h4>
            <div className="accessibility-options">
              <button 
                className={`accessibility-option ${!accessibilitySettings.screenReaderEnabled ? 'active' : ''}`}
                onClick={() => updateAccessibilitySetting('screenReaderEnabled', false)}
                aria-pressed={!accessibilitySettings.screenReaderEnabled}
              >
                Desactivar
              </button>
              <button 
                className={`accessibility-option ${accessibilitySettings.screenReaderEnabled ? 'active' : ''}`}
                onClick={() => updateAccessibilitySetting('screenReaderEnabled', true)}
                aria-pressed={accessibilitySettings.screenReaderEnabled}
              >
                Activar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Content Sections */}
      {activeTab === 'home' && (
        <div className="home-section">
          <div className="welcome-hero">
            <h2 className="welcome-title">👋 ¡Hola, Usuario!</h2>
            <p className="welcome-subtitle">¿Qué quieres aprender hoy?</p>
          </div>

          {/* Educational Level Selection */}
          <div className="level-selection">
            <h3 className="selection-title">🎓 Tu Nivel Educativo</h3>
            <div className="level-grid">
              {educationalLevels.map(level => (
                <button
                  key={level.id}
                  className={`level-card ${selectedLevel === level.id ? 'selected' : ''}`}
                  onClick={() => selectLevel(level.id)}
                  aria-label={`Seleccionar nivel educativo: ${level.name}`}
                  aria-pressed={selectedLevel === level.id}
                >
                  <span className="level-icon" aria-hidden="true">{level.icon}</span>
                  <span className="level-name">{level.name}</span>
                  <span className="level-desc">{level.description}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Time Selection */}
          <div className="time-selection">
            <h3 className="selection-title">⏱️ ¿Cuánto tiempo tienes?</h3>
            <div className="time-grid">
              {timeOptions.map(option => (
                <button
                  key={option.id}
                  className={`time-card ${selectedTime === option.id ? 'selected' : ''}`}
                  onClick={() => selectTime(option.id)}
                  aria-label={`Seleccionar tiempo: ${option.label}`}
                  aria-pressed={selectedTime === option.id}
                >
                  <span className="time-label">{option.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Daily Challenge */}
          <div className="daily-challenge-section">
            <h3 className="section-title">🎯 Reto del Día</h3>
            <div className="challenge-card">
              <div className="challenge-header">
                <span className="challenge-icon">⚡</span>
                <div className="challenge-info">
                  <h4>{dailyChallenge.title}</h4>
                  <p>{dailyChallenge.description}</p>
                </div>
              </div>
              <div className="challenge-rewards">
                <span className="reward-badge">⭐ +{dailyChallenge.xpReward} XP</span>
                <span className="reward-badge">🪙 +{dailyChallenge.coinsReward} Monedas</span>
              </div>
              <button 
                className="challenge-btn"
                onClick={completeDailyChallenge}
                disabled={dailyChallenge.completed}
              >
                {dailyChallenge.completed ? '✅ Completado' : '🚀 Aceptar Reto'}
              </button>
            </div>
          </div>

          {/* Quick Learning Activities */}
          <div className="quick-learning-section">
            <h3 className="section-title">⚡ Aprende en 5 Minutos</h3>
            <div className="quick-activities-grid">
              {quickActivities.map(activity => (
                <div key={activity.id} className="quick-activity-card">
                  <div className="activity-type-badge">{activity.type}</div>
                  <span className="activity-icon">{subjects.find(s => s.id === activity.subject)?.icon || '📚'}</span>
                  <h4>{activity.title}</h4>
                  <div className="activity-meta">
                    <span>⏱️ {activity.duration} min</span>
                    <span>⭐ +{activity.xpReward} XP</span>
                  </div>
                  <button 
                    className="activity-start-btn"
                    onClick={() => completeActivity(activity)}
                  >
                    Comenzar
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Amigis Companion */}
          <div className="amigis-companion-section">
            <h3 className="section-title">🤖 Amigis - Tu Compañero de Estudio</h3>
            <div className="amigis-card">
              <div className="amigis-avatar" role="img" aria-label="Amigis mascota zorro">🦊</div>
              <div className="amigis-message">
                <p>"¿No entendiste algo? Pregúntame y te explicaré de forma sencilla."</p>
              </div>
              <div className="amigis-actions">
                <button className="amigis-action-btn" aria-label="Explícame más fácil">💡 Explícame más fácil</button>
                <button className="amigis-action-btn" aria-label="Dame un ejemplo">🧠 Dame un ejemplo</button>
                <button className="amigis-action-btn" aria-label="Ponme un ejercicio">🎯 Ponme un ejercicio</button>
                <button className="amigis-action-btn" aria-label="Hazme preguntas">❓ Hazme preguntas</button>
              </div>
            </div>
          </div>

          {/* Adaptive Learning Options */}
          <div className="adaptive-learning-section">
            <h3 className="section-title">🧠 ¿Cómo prefieres aprender?</h3>
            <div className="adaptive-learning-options">
              <button className="adaptive-option" aria-label="Leer explicación" tabIndex={0}>
                <span className="adaptive-icon" aria-hidden="true">📖</span>
                <span className="adaptive-label">Leer explicación</span>
              </button>
              <button className="adaptive-option" aria-label="Escuchar explicación" tabIndex={0}>
                <span className="adaptive-icon" aria-hidden="true">🔊</span>
                <span className="adaptive-label">Escuchar explicación</span>
              </button>
              <button className="adaptive-option" aria-label="Ver explicación" tabIndex={0}>
                <span className="adaptive-icon" aria-hidden="true">🎥</span>
                <span className="adaptive-label">Ver explicación</span>
              </button>
              <button className="adaptive-option" aria-label="Aprender mediante actividad" tabIndex={0}>
                <span className="adaptive-icon" aria-hidden="true">🧩</span>
                <span className="adaptive-label">Aprender mediante actividad</span>
              </button>
              <button className="adaptive-option" aria-label="Explicación sencilla" tabIndex={0}>
                <span className="adaptive-icon" aria-hidden="true">💡</span>
                <span className="adaptive-label">Explicación sencilla</span>
              </button>
              <button className="adaptive-option" aria-label="Explicación detallada" tabIndex={0}>
                <span className="adaptive-icon" aria-hidden="true">📚</span>
                <span className="adaptive-label">Explicación detallada</span>
              </button>
            </div>
          </div>

          {/* Age Group Selection */}
          <div className="age-group-section">
            <h3 className="section-title">👤 Grupo de Edad (Opcional)</h3>
            <p className="section-subtitle">Esto ayuda a adaptar la dificultad y presentación del contenido</p>
            <div className="age-group-grid">
              {ageGroups.map(group => (
                <button
                  key={group.id}
                  className={`age-group-card ${selectedAgeGroup === group.id ? 'selected' : ''}`}
                  onClick={() => setSelectedAgeGroup(group.id)}
                  aria-label={`Seleccionar grupo de edad: ${group.name}`}
                  aria-pressed={selectedAgeGroup === group.id}
                  tabIndex={0}
                >
                  <span className="age-group-icon" aria-hidden="true">{group.icon}</span>
                  <span className="age-group-name">{group.name}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Learning Style Selection */}
          <div className="learning-style-section">
            <h3 className="section-title">🧠 Estilo de Aprendizaje (Opcional)</h3>
            <p className="section-subtitle">Personaliza cómo se presenta el contenido</p>
            <div className="learning-style-grid">
              {learningStyles.map(style => (
                <button
                  key={style.id}
                  className={`learning-style-card ${selectedLearningStyle === style.id ? 'selected' : ''}`}
                  onClick={() => setSelectedLearningStyle(style.id)}
                  aria-label={`Seleccionar estilo de aprendizaje: ${style.name}`}
                  aria-pressed={selectedLearningStyle === style.id}
                  tabIndex={0}
                >
                  <span className="learning-style-icon" aria-hidden="true">{style.icon}</span>
                  <span className="learning-style-name">{style.name}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'subjects' && (
        <div className="subjects-section">
          <h2 className="section-title">📚 Materias y Áreas de Conocimiento</h2>
          <div className="subjects-grid">
            {subjects.map(subject => (
              <div key={subject.id} className="subject-card">
                <span className="subject-icon">{subject.icon}</span>
                <h4>{subject.name}</h4>
                <span className="subject-category">{subject.category}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'activities' && (
        <div className="activities-section">
          <h2 className="section-title">🎮 Actividades Interactivas</h2>
          <div className="activity-types-grid">
            <div className="activity-type-card">
              <span className="activity-type-icon">🧠</span>
              <h4>Quiz</h4>
              <p>Preguntas de opción múltiple</p>
            </div>
            <div className="activity-type-card">
              <span className="activity-type-icon">🧩</span>
              <h4>Completar</h4>
              <p>Llena los espacios en blanco</p>
            </div>
            <div className="activity-type-card">
              <span className="activity-type-icon">🔤</span>
              <h4>Ordenar</h4>
              <p>Organiza palabras o conceptos</p>
            </div>
            <div className="activity-type-card">
              <span className="activity-type-icon">🎯</span>
              <h4>Seleccionar</h4>
              <p>Elige la respuesta correcta</p>
            </div>
            <div className="activity-type-card">
              <span className="activity-type-icon">🔗</span>
              <h4>Relacionar</h4>
              <p>Conecta conceptos relacionados</p>
            </div>
            <div className="activity-type-card">
              <span className="activity-type-icon">🃏</span>
              <h4>Flashcards</h4>
              <p>Tarjetas de memoria</p>
            </div>
            <div className="activity-type-card">
              <span className="activity-type-icon">🧪</span>
              <h4>Experimentos</h4>
              <p>Simulaciones virtuales</p>
            </div>
            <div className="activity-type-card">
              <span className="activity-type-icon">🗺️</span>
              <h4>Mapas</h4>
              <p>Mapas interactivos</p>
            </div>
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
              <button className="action-btn">📌 Nueva Nota</button>
              <button className="action-btn">🔍 Buscar</button>
              <button className="action-btn">📥 Exportar</button>
            </div>
          </div>
          <div className="notes-filters">
            <button className="filter-btn active">Todas</button>
            <button className="filter-btn">⭐ Favoritas</button>
            <button className="filter-btn">📚 Por Materia</button>
          </div>
          <div className="notes-list">
            {notes.map(note => (
              <div key={note.id} className="note-card">
                <div className="note-header">
                  <span className="note-pin">📌</span>
                  <span className="note-category">{note.category}</span>
                  <span className="note-date">{note.date}</span>
                </div>
                <h3>{note.title}</h3>
                <p>{note.content}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'progress' && (
        <div className="progress-section">
          <h2 className="section-title">📊 Mi Progreso</h2>
          <div className="progress-overview-grid">
            <div className="progress-overview-card">
              <span className="progress-icon">⭐</span>
              <div className="progress-value">{userProgress.xp}</div>
              <div className="progress-label">XP Total</div>
            </div>
            <div className="progress-overview-card">
              <span className="progress-icon">🪙</span>
              <div className="progress-value">{userProgress.coins}</div>
              <div className="progress-label">Monedas</div>
            </div>
            <div className="progress-overview-card">
              <span className="progress-icon">🔥</span>
              <div className="progress-value">{userProgress.streak} días</div>
              <div className="progress-label">Racha</div>
            </div>
            <div className="progress-overview-card">
              <span className="progress-icon">📚</span>
              <div className="progress-value">{userProgress.activitiesCompleted}</div>
              <div className="progress-label">Actividades</div>
            </div>
            <div className="progress-overview-card">
              <span className="progress-icon">⏱️</span>
              <div className="progress-value">{userProgress.hoursStudied}h</div>
              <div className="progress-label">Horas Estudiadas</div>
            </div>
            <div className="progress-overview-card">
              <span className="progress-icon">🏆</span>
              <div className="progress-value">Nivel {userProgress.level}</div>
              <div className="progress-label">Nivel Actual</div>
            </div>
          </div>

          <div className="badges-section">
            <h3 className="section-title">🏆 Insignias</h3>
            <div className="badges-grid">
              {userProgress.badges.map((badge, index) => (
                <div key={index} className="badge-card">
                  <span className="badge-emoji">{badge.split(' ')[0]}</span>
                  <span className="badge-name">{badge.split(' ').slice(1).join(' ')}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="weekly-progress-section">
            <h3 className="section-title">📈 Progreso Semanal</h3>
            <div className="weekly-chart">
              <div className="chart-bar" style={{ height: '60%' }}>
                <span className="bar-label">Lun</span>
              </div>
              <div className="chart-bar" style={{ height: '80%' }}>
                <span className="bar-label">Mar</span>
              </div>
              <div className="chart-bar" style={{ height: '45%' }}>
                <span className="bar-label">Mié</span>
              </div>
              <div className="chart-bar" style={{ height: '90%' }}>
                <span className="bar-label">Jue</span>
              </div>
              <div className="chart-bar" style={{ height: '70%' }}>
                <span className="bar-label">Vie</span>
              </div>
              <div className="chart-bar" style={{ height: '55%' }}>
                <span className="bar-label">Sáb</span>
              </div>
              <div className="chart-bar" style={{ height: '40%' }}>
                <span className="bar-label">Dom</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'academy' && (
        <div className="academy-section">
          <div className="academy-header">
            <h2>🎓 Academia de Amigis & Tienda de Accesorios</h2>
            <div className="coins-display">
              🪙 {userProgress.coins} Monedas Amigis
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
