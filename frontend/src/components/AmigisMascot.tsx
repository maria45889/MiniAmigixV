import { useState, useEffect, useRef } from 'react';
import './AmigisMascot.css';

interface AmigisMascotProps {
  onThemeChange?: (isLight: boolean) => void;
  onAIResponse?: () => void;
  onMusicPlay?: () => void;
  onWeatherLoad?: () => void;
  onGameStart?: () => void;
  onTranslation?: () => void;
}

const AmigisMascot: React.FC<AmigisMascotProps> = ({
  onThemeChange,
  onAIResponse,
  onMusicPlay,
  onWeatherLoad,
  onGameStart,
  onTranslation,
}) => {
  const [isTyping, setIsTyping] = useState(false);
  const [isHappy, setIsHappy] = useState(false);
  const [isCurious, setIsCurious] = useState(false);
  const [isWaving, setIsWaving] = useState(false);
  const [showBubble, setShowBubble] = useState(false);
  const [bubbleMessage, setBubbleMessage] = useState('');
  const [isLight, setIsLight] = useState(false);
  const bubbleTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const greetings = [
    '¡Hola! Soy Amigis, tu patito programador 🦆',
    '¡Qué gusto verte! ¿En qué puedo ayudarte?',
    '¡Hola amigo! Estoy listo para programar contigo',
    '¡Bienvenido! Soy Amigis, tu asistente de código',
    '¡Hey! ¿Listo para crear algo increíble?',
  ];

  const curiousMessages = [
    'Hmm... interesante 🤔',
    '¿Cómo funciona esto?',
    '¡Qué curioso!',
    'Me pregunto cómo hacerlo...',
    'Interesante... déjame pensar',
  ];

  const happyMessages = [
    '¡Genial! 🎉',
    '¡Excelente!',
    '¡Me encanta!',
    '¡Qué bien!',
    '¡Increíble!',
  ];

  useEffect(() => {
    // Saludo inicial
    const initialGreeting = setTimeout(() => {
      const randomGreeting = greetings[Math.floor(Math.random() * greetings.length)];
      showMessage(randomGreeting);
      setIsWaving(true);
      setTimeout(() => setIsWaving(false), 1500);
    }, 1500);

    // Detectar tema del sistema
    const mediaQuery = window.matchMedia('(prefers-color-scheme: light)');
    setIsLight(mediaQuery.matches);

    const handleThemeChange = (e: MediaQueryListEvent) => {
      setIsLight(e.matches);
    };

    mediaQuery.addEventListener('change', handleThemeChange);

    return () => {
      clearTimeout(initialGreeting);
      mediaQuery.removeEventListener('change', handleThemeChange);
      if (bubbleTimeoutRef.current) {
        clearTimeout(bubbleTimeoutRef.current);
      }
    };
  }, []);

  const showMessage = (message: string, duration: number = 4000) => {
    setBubbleMessage(message);
    setShowBubble(true);

    if (bubbleTimeoutRef.current) {
      clearTimeout(bubbleTimeoutRef.current);
    }

    bubbleTimeoutRef.current = setTimeout(() => {
      setShowBubble(false);
    }, duration);
  };

  const handleClick = () => {
    const allMessages = [...greetings, ...curiousMessages, ...happyMessages];
    const randomMessage = allMessages[Math.floor(Math.random() * allMessages.length)];
    showMessage(randomMessage);
    setIsHappy(true);
    setTimeout(() => setIsHappy(false), 600);
  };

  const handleMouseEnter = () => {
    setIsCurious(true);
  };

  const handleMouseLeave = () => {
    setIsCurious(false);
  };

  // Métodos públicos para eventos de la aplicación
  const triggerAIResponse = () => {
    setIsTyping(true);
    showMessage('Escribiendo código... 💻');
    setTimeout(() => {
      setIsTyping(false);
      setIsHappy(true);
      showMessage('¡Listo! Aquí está tu respuesta 🎉');
      setTimeout(() => setIsHappy(false), 600);
      if (onAIResponse) onAIResponse();
    }, 2000);
  };

  const triggerMusicPlay = () => {
    setIsHappy(true);
    showMessage('¡Música activada! 🎵');
    setTimeout(() => setIsHappy(false), 600);
    if (onMusicPlay) onMusicPlay();
  };

  const triggerWeatherLoad = () => {
    showMessage('¡Clima actualizado! ☀️');
    if (onWeatherLoad) onWeatherLoad();
  };

  const triggerGameStart = () => {
    setIsHappy(true);
    showMessage('¡Buena suerte! 🎮');
    setTimeout(() => setIsHappy(false), 600);
    if (onGameStart) onGameStart();
  };

  const triggerTranslation = () => {
    setIsTyping(true);
    setTimeout(() => {
      setIsTyping(false);
      showMessage('¡Traducción lista! 🌐');
      if (onTranslation) onTranslation();
    }, 1500);
  };

  // Exponer métodos globalmente para uso externo
  useEffect(() => {
    (window as any).AmigisReact = {
      triggerAIResponse,
      triggerMusicPlay,
      triggerWeatherLoad,
      triggerGameStart,
      triggerTranslation,
      showMessage,
      setHappy: () => {
        setIsHappy(true);
        setTimeout(() => setIsHappy(false), 600);
      },
      setCurious: (value: boolean) => setIsCurious(value),
      setTyping: (value: boolean) => setIsTyping(value),
    };
  }, []);

  return (
    <div className={`amigis-container ${isLight ? 'light-mode' : 'dark-mode'}`}>
      {showBubble && (
        <div className={`amigis-bubble ${showBubble ? 'show' : ''}`}>
          {bubbleMessage}
        </div>
      )}
      <div
        className={`amigis-wrapper ${isTyping ? 'typing' : ''} ${isHappy ? 'happy' : ''} ${isCurious ? 'curious' : ''}`}
        onClick={handleClick}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        {/* Cola */}
        <div className="amigis-tail" />

        {/* Cuerpo */}
        <div className="amigis-body" />

        {/* Patitas */}
        <div className="amigis-foot left" />
        <div className="amigis-foot right" />

        {/* Alas */}
        <div className="amigis-wing left" />
        <div className={`amigis-wing right ${isWaving ? 'waving' : ''}`} />

        {/* Cabeza */}
        <div className={`amigis-head ${isCurious ? 'curious' : ''}`}>
          {/* Gorra */}
          <div className="amigis-cap" />

          {/* Ojos */}
          <div className="amigis-eye left">
            <div className="amigis-pupil" />
            <div className="amigis-eyelash left" />
          </div>
          <div className="amigis-eye right">
            <div className="amigis-pupil" />
            <div className="amigis-eyelash right" />
          </div>

          {/* Mejillas */}
          <div className={`amigis-cheek left ${isHappy ? 'show' : ''}`} />
          <div className={`amigis-cheek right ${isHappy ? 'show' : ''}`} />

          {/* Pico */}
          <div className="amigis-beak" />
        </div>

        {/* Laptop */}
        <div className={`amigis-laptop ${isTyping ? 'show' : ''}`}>
          <div className="amigis-laptop-screen">
            <div className="amigis-laptop-code">
              <div className="amigis-code-line" />
              <div className="amigis-code-line" />
              <div className="amigis-code-line" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AmigisMascot;
