# 🦆 Amigis - Versión Simple y Escalable

## ¿Qué es Amigis?

Amigis es la mascota oficial de MiniAmigixV: un patito programador amigable que acompaña a los usuarios en todas las secciones de la plataforma.

## Características (Versión Simple)

- ✨ **Animación suave**: Flotación constante
- 🌙☀️ **Cambio de tema**: Imagen SVG que cambia según modo claro/oscuro
- 💬 **Burbujas de diálogo**: Mensajes contextuales
- 🎉 **Animaciones reactivas**: Responde a eventos de la aplicación
- 📱 **Responsive**: Se adapta a dispositivos móviles

## Estructura de Archivos

```
static/amigis/
├── amigis-light.svg      # SVG para modo claro
├── amigis-dark.svg       # SVG para modo oscuro
├── css/
│   └── amigis.css        # Estilos y animaciones
└── js/
    └── amigis.js         # Lógica JavaScript
```

## Integración Automática

Amigis se carga automáticamente en `base.html`, por lo que está disponible en todas las páginas que heredan de este template.

## Métodos Disponibles

```javascript
// Obtener instancia de Amigis
const amigis = window.Amigis;

// Mostrar mensaje personalizado
amigis.showMessage('¡Hola! ¿En qué puedo ayudarte?', 4000);

// Activar animación feliz
amigis.setHappy();

// Activar animación de escribir
amigis.setTyping(true);
amigis.setTyping(false);

// Activar animación de pensar
amigis.setThinking(true);
amigis.setThinking(false);

// Eventos específicos
amigis.onAIWriting();      // Cuando la IA está escribiendo
amigis.onAIFinished();     // Cuando la IA termina
amigis.onSectionChange('chat'); // Al cambiar de sección
```

## Ejemplos de Integración

### Chat IA

```javascript
// Cuando el usuario envía un mensaje
document.getElementById('send-btn').addEventListener('click', () => {
    if (window.Amigis) {
        window.Amigis.onAIWriting();
    }
});

// Cuando la IA responde
function onAIResponse() {
    if (window.Amigis) {
        window.Amigis.onAIFinished();
    }
}
```

### Cambio de Sección

```javascript
// Detectar cambio de sección
function detectSection() {
    const path = window.location.pathname;
    let section = 'home';
    
    if (path.includes('chat')) section = 'chat';
    else if (path.includes('musica')) section = 'musica';
    else if (path.includes('juegos')) section = 'juegos';
    // ... más secciones
    
    if (window.Amigis) {
        window.Amigis.onSectionChange(section);
    }
}
```

## Animaciones Disponibles

### CSS

- `float`: Flotación suave (activa por defecto)
- `typing`: Rebote suave cuando escribe
- `happy`: Saltito de alegría
- `thinking`: Balanceo lateral

### Estados del Componente

- `typing`: Muestra animación de escribir
- `happy`: Muestra saltito de alegría
- `thinking`: Muestra balanceo de pensamiento

## Personalización

### Cambiar Imágenes

Los archivos SVG están en `static/amigis/`:
- `amigis-light.svg` - Para modo claro
- `amigis-dark.svg` - Para modo oscuro

Puedes editar estos archivos SVG para cambiar el diseño del patito.

### Cambiar Mensajes

Edita el archivo `static/amigis/js/amigis.js`:

```javascript
this.greetings = [
    '¡Hola! Soy Amigis, tu patito programador 🦆',
    '¡Qué gusto verte! ¿En qué puedo ayudarte?',
    // Agrega más saludos personalizados
];

this.sectionMessages = {
    'home': '¡Estás en el inicio! 🏠',
    'chat': '¡Hablemos! 💬',
    // Personaliza mensajes por sección
};
```

### Agregar Nuevas Animaciones CSS

En `static/amigis/css/amigis.css`:

```css
/* Nueva animación */
@keyframes miAnimacion {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.1);
    }
}

.amigis-wrapper.mi-animacion {
    animation: miAnimacion 0.5s ease-in-out;
}
```

Luego en JavaScript:

```javascript
// En static/amigis/js/amigis.js
setMiAnimacion() {
    if (this.wrapper) {
        this.wrapper.classList.add('mi-animacion');
        setTimeout(() => {
            this.wrapper.classList.remove('mi-animacion');
        }, 500);
    }
}
```

## Próximos Pasos (Mejoras Progresivas)

1. **Más expresiones SVG**: Crear variantes del SVG para diferentes expresiones
2. **Accesorios por sección**: Agregar elementos SVG específicos (audífonos, paraguas, etc.)
3. **Animaciones más complejas**: Usar SVG animations o Lottie
4. **Interactividad mejorada**: Arrastrar, soltar, más interacciones
5. **Sonidos**: Efectos de sonido opcionales
6. **Voz**: Síntesis de voz para mensajes

## Troubleshooting

### La mascota no aparece

1. Verifica que los archivos CSS y JS estén cargados en `base.html`
2. Revisa la consola del navegador para errores
3. Asegúrate de que los archivos SVG existan en `static/amigis/`

### La imagen no cambia de tema

1. Verifica que la clase `light` se agregue/elimine del `body`
2. Revisa las rutas de los archivos SVG en `amigis.js`
3. Asegúrate de que los archivos SVG tengan nombres correctos

### Las animaciones no funcionan

1. Verifica que el navegador soporte las animaciones CSS
2. Revisa que las clases CSS se apliquen correctamente
3. Verifica que no haya conflictos con otros estilos

## Ventajas de este Enfoque

✅ **Simple**: Fácil de entender y mantener  
✅ **Escalable**: Fácil agregar nuevas características  
✅ **Performante**: SVG ligero, animaciones CSS eficientes  
✅ **Flexible**: Fácil personalizar sin rehacer todo  
✅ **Progresivo**: Mejoras incrementales sin romper lo existente  

---

**¡Disfruta de Amigis, tu patito programador! 🦆✨**
