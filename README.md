# MiniAmigixV

Una aplicación web integral que combina múltiples funcionalidades: Chat IA, Eventos, Música, Clima, Juegos, Antiestrés, Estudios, Entretenimiento, Traductor, Blog, Configuración, Ayuda IA, Notificaciones, modo claro/oscuro, sugerencias, tutorial, autenticación, perfil de usuario, reloj en tiempo real y más.

## Estructura del Proyecto

```
miniamigixv/
├── index.html                 # Página de inicio
├── css/
│   ├── styles.css             # Estilos principales
│   └── theme.css              # Tema claro/oscuro
├── js/
│   ├── main.js                # Lógica principal
│   ├── chat.js                # Chat IA
│   ├── events.js              # Gestión de eventos
│   ├── music.js               # Reproductor de música
│   ├── weather.js             # Información del clima
│   ├── games.js               # Juegos integrados
│   ├── antiestres.js          # Herramientas antiestrés
│   ├── estudios.js            # Recursos de estudio
│   ├── entretenimiento.js     # Contenido de entretenimiento
│   ├── translator.js          # Traductor multiidioma
│   ├── blog.js                # Sistema de blog
│   ├── config.js              # Configuración de usuario
│   ├── aiHelp.js              # Asistente IA
│   ├── notifications.js       # Sistema de notificaciones
│   ├── suggestions.js         # Sugerencias inteligentes
│   ├── tutorial.js            # Tutorial interactivo
│   ├── auth.js                # Login, registro, cerrar sesión
│   ├── profile.js             # Perfil de usuario
│   └── clock.js               # Reloj en tiempo real
├── assets/
│   ├── images/                # Imágenes e íconos
│   ├── icons/
│   └── sounds/                # Efectos de sonido y música
├── pages/                     # Páginas individuales (opcional para MPA)
│   ├── inicio.html
│   ├── chat.html
│   ├── eventos.html
│   ├── musica.html
│   ├── clima.html
│   ├── juegos.html
│   ├── antiestres.html
│   ├── estudios.html
│   ├── entretenimiento.html
│   ├── traductor.html
│   ├── blog.html
│   ├── configuracion.html
│   ├── ayuda.html
│   ├── notificaciones.html
│   ├── perfil.html
│   └── tutorial.html
├── blog/
│   └── posts/                 # Entradas del blog (markdown o HTML)
└── data/                      #Datos locales (JSON, etc.)
    ├── usuarios.json
    ├── eventos.json
    └── configuracion.json
```

## Características Principales

- **Interfaz moderna y responsive** - Diseño adaptable a móviles, tablet y escritorio
- **Modo claro/oscuro** - Preferencia guardada en localStorage
- **Autenticación completa** - Login, registro, perfil y cierre de sesión
- **Chat IA integrado** - Conversaciones con inteligencia artificial
- **Calendario de eventos** - Creación, edición y recordatorios
- **Reproductor de música** - Con playlists y controles
- **Información del clima** - En tiempo real basada en ubicación
- **Juegos casuales** - Para entretenimiento rápido
- **Herramientas antiestrés** - Meditación, respiración, juegos relajantes
- **Recursos de estudio** - Flashcards, apuntes, calculadoras
- **Sección de entretenimiento** - Videos, memes, noticias ligeras
- **Traductor multiidioma** - Traducción instantánea
- **Sistema de blog** - Artículos, comentarios y categorías
- **Centro de ayuda IA** - Asistente para resolver dudas
- **Notificaciones en tiempo real** - Alertas y recordatorios
- **Sugerencias inteligentes** - Basadas en uso y preferencias
- **Tutorial interactivo** - Guía para nuevos usuarios
- **Reloj en tiempo real** - Con fecha y zona horaria
- **Perfil de usuario personalizable** - Avatar, datos y preferencias

## Tecnologías Utilizadas

- HTML5 semántico
- CSS3 con variables y flexbox/grid
- JavaScript Vanilla (ES6+) o framework según preferencia
- LocalStorage para persistencia de datos
- APIs externas (clima, traducción, etc.) según disponibilidad
- Diseño mobile-first

## Instalación y Uso

1. Clonar o descargar este repositorio
2. Abrir `index.html` en cualquier navegador moderno
3. (Opcional) Configurar claves API para servicios externos en `config.js`
4. Disfrutar de todas las funcionalidades

## Personalización

- Modificar colores en `css/theme.css`
- Añadir nuevos juegos en la carpeta `js/games.js` y `assets/sounds/`
- Agregar artículos al blog en `blog/posts/`
- Configurar preferencias por defecto en `data/configuracion.json`

## Contribuir

¡Las contribuciones son bienvenidas! Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Haz tus cambios y commitea (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la licencia MIT - ver el archivo LICENSE para más detalles.

## Contacto

Desarrollado por Majo 💕
Para soporte o sugerencias, usa el sistema de Ayuda IA dentro de la aplicación o abre un issue.

¡Disfruta de MiniAmigixV!