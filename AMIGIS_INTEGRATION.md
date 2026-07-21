# 🦆 Amigis - Guía de Integración

## ¿Qué es Amigis?

Amigis es la mascota oficial de MiniAmigixV: un patito programador amigable y curioso que acompaña a los usuarios en todas las secciones de la plataforma.

## Características

- ✨ **Animaciones suaves**: Flotación, parpadeo, saludos y expresiones
- 💻 **Laptop interactiva**: Aparece cuando la IA responde
- 🌙☀️ **Modo claro/oscuro**: Cambia de color automáticamente
- 👀 **Ojos que siguen el cursor**: Interacción dinámica
- 🎉 **Reacciones a eventos**: Responde a acciones del usuario
- 💬 **Burbujas de diálogo**: Mensajes contextuales

## Arquitectura

### Archivos Creados

1. **CSS**: `static/css/core/amigis.css`
   - Estilos para el patito, animaciones y temas
   - Variables CSS para modo claro/oscuro

2. **JavaScript**: `static/js/amigis.js`
   - Clase `AmigisMascot` para templates Django
   - Integración automática en `base.html`

3. **React Component**: `frontend/src/components/AmigisMascot.tsx`
   - Componente React con TypeScript
   - Props para eventos de la aplicación

4. **React CSS**: `frontend/src/components/AmigisMascot.css`
   - Estilos específicos para el componente React

## Integración en Templates Django

### Uso Básico

La mascota se carga automáticamente en `base.html`, por lo que está disponible en todas las páginas que heredan de este template.

### Métodos Disponibles (JavaScript)

```javascript
// Obtener instancia de Amigis
const amigis = window.Amigis;

// Mostrar mensaje personalizado
amigis.showMessage('¡Hola! ¿En qué puedo ayudarte?', 4000);

// Activar estado feliz
amigis.setHappy();

// Activar estado curioso
amigis.setCurious(true);
amigis.setCurious(false);

// Activar estado de escritura (con laptop)
amigis.setTyping(true);
amigis.setTyping(false);

// Eventos específicos
amigis.onAIResponse();      // Cuando la IA responde
amigis.onMusicPlay();       // Cuando se reproduce música
amigis.onWeatherLoad();     // Cuando se carga el clima
amigis.onGameStart();       // Cuando inicia un juego
amigis.onTranslation();     // Cuando se traduce texto
```

### Ejemplos de Integración por Sección

#### 1. Chat IA

```html
<!-- En tu template de chat -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.getElementById('send-message-btn');
    
    sendButton.addEventListener('click', function() {
        // Activar animación de escritura
        if (window.Amigis) {
            window.Amigis.setTyping(true);
        }
    });
    
    // Cuando la IA responda
    function onAIResponse() {
        if (window.Amigis) {
            window.Amigis.onAIResponse();
        }
    }
});
</script>
```

#### 2. Música

```html
<!-- En tu template de música -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    const playButton = document.getElementById('play-btn');
    
    playButton.addEventListener('click', function() {
        if (window.Amigis) {
            window.Amigis.onMusicPlay();
        }
    });
});
</script>
```

#### 3. Clima

```html
<!-- En tu template de clima -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    function loadWeather() {
        // Tu lógica de clima
        fetchWeatherData().then(() => {
            if (window.Amigis) {
                window.Amigis.onWeatherLoad();
            }
        });
    }
});
</script>
```

#### 4. Juegos

```html
<!-- En tu template de juegos -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    const startButton = document.getElementById('start-game-btn');
    
    startButton.addEventListener('click', function() {
        if (window.Amigis) {
            window.Amigis.onGameStart();
        }
    });
});
</script>
```

#### 5. Traductor

```html
<!-- En tu template de traductor -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    const translateButton = document.getElementById('translate-btn');
    
    translateButton.addEventListener('click', function() {
        if (window.Amigis) {
            window.Amigis.onTranslation();
        }
    });
});
</script>
```

#### 6. Tutoriales/Soporte

```html
<!-- En tu template de tutoriales -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Cuando el usuario abra un tutorial
    function openTutorial(tutorialId) {
        if (window.Amigis) {
            window.Amigis.showMessage('¡Excelente elección! Vamos a aprender 📚', 5000);
        }
    }
});
</script>
```

## Integración en React

### Uso en Componentes React

```tsx
import AmigisMascot from './components/AmigisMascot';

function MiComponente() {
  const handleAIResponse = () => {
    console.log('IA respondió');
  };

  return (
    <div>
      {/* Tu contenido */}
      
      <AmigisMascot
        onAIResponse={handleAIResponse}
        onMusicPlay={() => console.log('Música activada')}
        onWeatherLoad={() => console.log('Clima actualizado')}
        onGameStart={() => console.log('Juego iniciado')}
        onTranslation={() => console.log('Traducción completada')}
      />
    </div>
  );
}
```

### Métodos Públicos (React)

```tsx
// Acceder a los métodos de Amigis
const amigisReact = (window as any).AmigisReact;

// Mostrar mensaje
amigisReact.showMessage('Mensaje personalizado');

// Activar estados
amigisReact.setHappy();
amigisReact.setCurious(true);
amigisReact.setTyping(true);

// Trigger eventos
amigisReact.triggerAIResponse();
amigisReact.triggerMusicPlay();
amigisReact.triggerWeatherLoad();
amigisReact.triggerGameStart();
amigisReact.triggerTranslation();
```

## Personalización

### Colores del Tema

Los colores se definen mediante variables CSS en `amigis.css`:

```css
/* Modo Claro */
body.light {
    --amigis-primary: #FFD93D;
    --amigis-secondary: #FFC107;
    --amigis-beak: #FF6B35;
    --amigis-laptop: #718096;
    --amigis-cap: #805AD5;
}

/* Modo Oscuro */
body:not(.light) {
    --amigis-primary: #FFD700;
    --amigis-secondary: #FFC107;
    --amigis-beak: #FF6B35;
    --amigis-laptop: #4A5568;
    --amigis-cap: #7C3AED;
}
```

### Mensajes Personalizados

Puedes personalizar los mensajes en `amigis.js`:

```javascript
this.greetings = [
    '¡Hola! Soy Amigis, tu patito programador 🦆',
    '¡Qué gusto verte! ¿En qué puedo ayudarte?',
    // Agrega más saludos personalizados
];

this.curiousMessages = [
    'Hmm... interesante 🤔',
    // Agrega más mensajes curiosos
];

this.happyMessages = [
    '¡Genial! 🎉',
    // Agrega más mensajes felices
];
```

## Animaciones Disponibles

### Animaciones CSS

- `blink`: Parpadeo de ojos
- `float`: Flotación suave
- `typing`: Líneas de código en la laptop
- `wave`: Saludo con el ala
- `curious`: Inclinación de cabeza
- `happy`: Saltito de alegría

### Estados del Componente

- `typing`: Muestra la laptop y animación de código
- `happy`: Muestra mejillas sonrojadas y saltito
- `curious`: Inclina la cabeza
- `waving`: Mueve el ala derecho

## Responsive Design

La mascota se adapta automáticamente a dispositivos móviles:

- Desktop: 120px × 120px
- Mobile: 100px × 100px
- Burbuja de diálogo ajustada para pantallas pequeñas

## Accesibilidad

- La mascota es decorativa y no interfiere con la navegación
- Se puede ocultar si es necesario mediante CSS
- Los mensajes son visuales y no dependen de audio

## Troubleshooting

### La mascota no aparece

1. Verifica que `amigis.css` y `amigis.js` estén cargados en `base.html`
2. Revisa la consola del navegador para errores
3. Asegúrate de que no haya conflictos con otros scripts

### Los colores no cambian

1. Verifica que la clase `light` se agregue/elimine del `body`
2. Revisa las variables CSS en `amigis.css`
3. Asegúrate de que el tema se guarde correctamente

### Las animaciones no funcionan

1. Verifica que el navegador soporte las animaciones CSS
2. Revisa que no haya `prefers-reduced-motion` activado
3. Verifica que las clases CSS se apliquen correctamente

## Próximos Pasos

1. **Integrar en todas las secciones**: Agregar los eventos específicos en cada template
2. **Personalizar mensajes**: Adaptar los mensajes a cada sección
3. **Agregar más animaciones**: Crear animaciones específicas para cada acción
4. **Sonidos**: Agregar efectos de sonido opcionales
5. **Interacciones adicionales**: Permitir que Amigis arrastre elementos o interactúe más

## Soporte

Si encuentras algún problema o tienes sugerencias para mejorar Amigis, por favor crea un issue en el repositorio del proyecto.

---

**¡Disfruta de Amigis, tu patito programador! 🦆💻✨**
