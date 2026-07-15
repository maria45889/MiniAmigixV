# Arquitectura Limpia - MiniAmigixV

## Resumen de la Refactorización

Se ha implementado una arquitectura limpia profesional en `apps/app/` siguiendo los principios de separación de responsabilidades con estructura basada en carpetas. El archivo `views.py` original de más de 2200 líneas se ha reorganizado en múltiples módulos especializados distribuidos en carpetas.

## Estructura de Archivos

```
apps/app/
├── __init__.py
├── admin.py              # Admin Django (sin cambios)
├── apps.py               # Configuración de la app Django (sin cambios)
├── models.py             # Modelos Django (sin cambios)
├── urls.py               # URLs Django (sin cambios)
├── views.py              # Vistas HTTP (capa de compatibilidad)
├── constants.py          # Datos estáticos (legacy - migrado a constants/)
├── selectors.py          # Consultas ORM (legacy - migrado a selectors/)
├── services.py           # Lógica de negocio (legacy - migrado a services/)
├── utils.py              # Funciones auxiliares (legacy - migrado a utils/)
├── exceptions.py         # Excepciones personalizadas (legacy)
├── validators.py         # Validaciones (legacy)
├── permissions.py       # Permisos (sin cambios)
├── signals.py            # Señales Django (sin cambios)
├── tasks.py              # Tareas Celery (sin cambios)
├── adapters.py           # Adaptadores Django Allauth (sin cambios)
├── middleware.py         # Middleware personalizado (sin cambios)
│
├── services/             # Lógica de negocio organizada por dominio
│   ├── __init__.py
│   ├── auth_service.py
│   ├── chat_service.py
│   ├── entertainment_service.py
│   ├── music_service.py
│   ├── weather_service.py
│   ├── translate_service.py
│   ├── study_service.py
│   ├── calendar_service.py
│   ├── notification_service.py
│   └── user_service.py
│
├── selectors/            # Consultas ORM organizadas por dominio
│   ├── __init__.py
│   ├── auth_selector.py
│   ├── chat_selector.py
│   ├── music_selector.py
│   ├── weather_selector.py
│   ├── study_selector.py
│   ├── entertainment_selector.py
│   ├── calendar_selector.py
│   ├── user_selector.py
│   └── notification_selector.py
│
├── api/                  # Integraciones con APIs externas
│   ├── __init__.py
│   ├── openai_api.py
│   ├── weather_api.py
│   ├── youtube_api.py
│   ├── spotify_api.py
│   ├── gemini_api.py
│   └── translator_api.py
│
├── constants/            # Constantes organizadas por categoría
│   ├── __init__.py
│   ├── chat.py
│   ├── entertainment.py
│   ├── messages.py
│   ├── prompts.py
│   └── settings.py
│
├── prompts/              # Prompts de IA organizados por funcionalidad
│   ├── __init__.py
│   ├── chat.py
│   ├── translator.py
│   ├── study.py
│   └── entertainment.py
│
├── repositories/         # Capa de acceso a datos
│   ├── __init__.py
│   ├── chat_repository.py
│   ├── music_repository.py
│   ├── weather_repository.py
│   ├── study_repository.py
│   └── user_repository.py
│
├── serializers/          # Serializers Django REST Framework
│   ├── __init__.py
│   ├── user_serializer.py
│   ├── chat_serializer.py
│   ├── music_serializer.py
│   └── calendar_serializer.py
│
├── forms/                # Formularios Django
│   ├── __init__.py
│   ├── login_form.py
│   ├── register_form.py
│   └── profile_form.py
│
├── views/                # Vistas HTTP organizadas por dominio
│   ├── __init__.py
│   ├── auth_views.py
│   ├── chat_views.py
│   ├── home_views.py
│   ├── music_views.py
│   ├── calendar_views.py
│   ├── weather_views.py
│   ├── study_views.py
│   ├── entertainment_views.py
│   └── profile_views.py
│
├── frontend/             # Componentes React TypeScript
│   ├── __init__.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   ├── Modal.tsx
│   │   └── LoadingSpinner.tsx
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── ChatPage.tsx
│   │   └── HomePage.tsx
│   ├── hooks/
│   │   ├── __init__.py
│   │   ├── useAuth.ts
│   │   └── useTheme.ts
│   └── utils/
│       ├── __init__.py
│       ├── api.ts
│       └── format.ts
│
├── templates/            # Templates Django (sin cambios)
│   └── app/
│
├── static/               # Archivos estáticos (sin cambios)
│   └── app/
│
└── migrations/           # Migraciones Django (sin cambios)
```

## Descripción de Carpetas y Módulos

### services/ - Lógica de Negocio
Contiene la lógica de negocio organizada por dominio:

- **auth_service.py**: Registro, login, logout de usuarios
- **chat_service.py**: Gestión de conversaciones, mensajes, respuestas IA
- **entertainment_service.py**: Recomendaciones de entretenimiento
- **music_service.py**: Gestión de playlists, canciones, favoritos
- **weather_service.py**: Consultas de clima
- **translate_service.py**: Traducción de texto
- **study_service.py**: Gestión de recursos de estudio
- **calendar_service.py**: Gestión de eventos y calendario
- **notification_service.py**: Creación y gestión de notificaciones
- **user_service.py**: Estadísticas y perfil de usuario

### selectors/ - Consultas ORM
Contiene las consultas a la base de datos organizadas por dominio:

- **auth_selector.py**: Consultas de autenticación (usuarios, emails, social apps)
- **chat_selector.py**: Consultas de conversaciones y mensajes
- **music_selector.py**: Consultas de música (canciones, playlists, favoritos)
- **weather_selector.py**: Consultas de caché de clima
- **study_selector.py**: Consultas de recursos de estudio
- **entertainment_selector.py**: Consultas de preferencias de entretenimiento
- **calendar_selector.py**: Consultas de eventos y calendario
- **user_selector.py**: Consultas de usuarios
- **notification_selector.py**: Consultas de notificaciones

### api/ - Integraciones Externas
Contiene las integraciones con APIs de terceros:

- **openai_api.py**: Integración con OpenAI API (chat, visión)
- **weather_api.py**: Integración con OpenWeatherMap
- **youtube_api.py**: Integración con YouTube (yt-dlp)
- **spotify_api.py**: Integración con Spotify (placeholder)
- **gemini_api.py**: Integración con Google Gemini (placeholder)
- **translator_api.py**: Integración con Google Translate

### constants/ - Constantes
Contiene datos estáticos organizados por categoría:

- **chat.py**: Configuraciones de chat, eventos, mensajes por defecto
- **entertainment.py**: Recomendaciones de películas, series, anime, libros
- **messages.py**: Mensajes de error y éxito
- **prompts.py**: Prompts del sistema de IA
- **settings.py**: Configuraciones generales (formatos de fecha, límites)

### prompts/ - Prompts de IA
Contiene prompts de IA organizados por funcionalidad:

- **chat.py**: Prompt principal del asistente MiniAmigix
- **translator.py**: Prompt para traducción
- **study.py**: Prompt para tutor educativo
- **entertainment.py**: Prompt para recomendaciones de entretenimiento

### repositories/ - Acceso a Datos
Contiene la capa de acceso a datos para operaciones complejas:

- **chat_repository.py**: Operaciones de persistencia de chat
- **music_repository.py**: Operaciones de persistencia de música
- **weather_repository.py**: Operaciones de caché de clima
- **study_repository.py**: Operaciones de persistencia de estudio
- **user_repository.py**: Operaciones de persistencia de usuarios

### serializers/ - Serializers DRF
Contiene serializadores para Django REST Framework:

- **user_serializer.py**: Serializadores de usuario (UserSerializer, UserCreateSerializer)
- **chat_serializer.py**: Serializadores de chat (ChatSerializer, MessageSerializer)
- **music_serializer.py**: Serializadores de música (SongSerializer, PlaylistSerializer)
- **calendar_serializer.py**: Serializadores de calendario (EventSerializer)

### forms/ - Formularios Django
Contiene formularios Django para validación:

- **login_form.py**: Formulario de inicio de sesión
- **register_form.py**: Formulario de registro
- **profile_form.py**: Formulario de actualización de perfil

### views/ - Vistas HTTP
Contiene las vistas HTTP organizadas por dominio:

- **auth_views.py**: Vistas de autenticación (login, register, logout)
- **chat_views.py**: Vistas de chat (chat_view, chat_api)
- **home_views.py**: Vistas principales (home, index)
- **music_views.py**: Vistas de música (musica, crear_playlist, agregar_a_playlist, toggle_favorito)
- **calendar_views.py**: Vistas de calendario (eventos)
- **weather_views.py**: Vistas de clima (clima)
- **study_views.py**: Vistas de estudio (estudio)
- **entertainment_views.py**: Vistas de entretenimiento (entretenimiento)
- **profile_views.py**: Vistas de perfil (perfil, configuración)

### frontend/ - Componentes React TypeScript
Contiene componentes React para el frontend:

- **components/**: Componentes reutilizables (Button, Input, Card, Modal, LoadingSpinner)
- **pages/**: Páginas completas (ChatPage, HomePage)
- **hooks/**: Hooks personalizados (useAuth, useTheme)
- **utils/**: Utilidades de frontend (api, format)

## Archivos Legacy (Mantenidos por Compatibilidad)

Los siguientes archivos se mantienen por compatibilidad pero están marcados como legacy:

- **constants.py**: Datos estáticos (migrado a constants/)
- **selectors.py**: Consultas ORM (migrado a selectors/)
- **services.py**: Lógica de negocio (migrado a services/)
- **utils.py**: Funciones auxiliares (migrado a utils/)
- **exceptions.py**: Excepciones personalizadas (migrado a exceptions/)
- **validators.py**: Validaciones (migrado a validators/)
- **views.py**: Ahora es una capa de compatibilidad que importa desde views/

## Beneficios de la Nueva Arquitectura

### 1. Separación de Responsabilidades
Cada módulo tiene una responsabilidad clara y única:
- **services/**: Lógica de negocio pura
- **selectors/**: Consultas a la base de datos
- **api/**: Integraciones externas
- **constants/**: Datos estáticos
- **views/**: Manejo de HTTP

### 2. Escalabilidad
La estructura basada en carpetas permite:
- Agregar nuevos servicios sin afectar otros módulos
- Organizar código por dominio funcional
- Mantener archivos pequeños y manejables

### 3. Testabilidad
Cada módulo puede ser testeado independientemente:
- Services pueden ser testeados con mocks
- Selectors pueden ser testeados con fixtures
- Views pueden ser testeados con clientes HTTP

### 4. Mantenibilidad
El código es más fácil de:
- Entender (archivos más pequeños y enfocados)
- Modificar (cambios localizados)
- Depurar (seguimiento claro del flujo de datos)

### 5. Reutilización
Los módulos pueden ser reutilizados en:
- Otras apps Django del proyecto
- Proyectos futuros
- APIs REST independientes

## Configuración de Python Path

Se ha actualizado `config/settings.py` para incluir las nuevas carpetas en el Python path:

```python
# Add apps/app/ subdirectories to Python path for folder-based structure
sys.path.insert(0, str(BASE_DIR / 'apps' / 'app' / 'services'))
sys.path.insert(0, str(BASE_DIR / 'apps' / 'app' / 'selectors'))
sys.path.insert(0, str(BASE_DIR / 'apps' / 'app' / 'api'))
sys.path.insert(0, str(BASE_DIR / 'apps' / 'app' / 'constants'))
sys.path.insert(0, str(BASE_DIR / 'apps' / 'app' / 'prompts'))
sys.path.insert(0, str(BASE_DIR / 'apps' / 'app' / 'repositories'))
sys.path.insert(0, str(BASE_DIR / 'apps' / 'app' / 'serializers'))
sys.path.insert(0, str(BASE_DIR / 'apps' / 'app' / 'forms'))
sys.path.insert(0, str(BASE_DIR / 'apps' / 'app' / 'views'))
```

## Compatibilidad Backward

El archivo `views.py` original ahora funciona como una capa de compatibilidad:

```python
# Import all views from the new views/ folder structure
from .views.auth_views import login_view, register_view, logout_view
from .views.chat_views import chat_view, chat_api
from .views.home_views import home, index
# ... etc
```

Esto asegura que:
- Las URLs existentes sigan funcionando sin cambios
- Los templates existentes sigan funcionando sin cambios
- Las APIs existentes sigan funcionando sin cambios
- No se requiere migración inmediata de código externo

## Próximos Pasos

1. **Migrar código legacy**: Gradualmente migrar código de archivos legacy a las nuevas carpetas
2. **Actualizar imports**: Cambiar imports en el código para usar las nuevas carpetas
3. **Eliminar archivos legacy**: Una vez que todo esté migrado, eliminar archivos legacy
4. **Testing**: Crear tests unitarios para cada módulo
5. **Documentación**: Actualizar documentación de API y desarrollo

## Notas sobre TypeScript/React

Los archivos TSX en `frontend/` son componentes React TypeScript preparados para:
- Integración con el backend Django REST API
- Sistema de temas (claro/oscuro)
- Gestión de estado con hooks personalizados
- Componentes reutilizables con TypeScript para type safety

**Nota**: Los errores de linting de TypeScript son esperados ya que React no está instalado en este proyecto Django. Estos componentes están preparados para cuando se implemente el frontend React.
