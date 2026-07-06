<div align="center">

# 🚀 MiniAmigixV

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0.6-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

**Una plataforma web moderna de productividad con IA, diseño glassmorphism y múltiples herramientas inteligentes integradas.**

[Demo](#) • [Reportar Bug](#) • [Solicitar Feature](#)

</div>

---

## 📖 Sobre MiniAmigixV

MiniAmigixV es una aplicación web revolucionaria desarrollada con **Django** que integra múltiples herramientas inteligentes en una sola plataforma. Ofrece una experiencia visual excepcional con diseño **glassmorphism**, interfaz completamente responsiva y funcionalidades potenciadas por Inteligencia Artificial.

### 🎯 Visión

Crear un ecosistema digital donde usuarios puedan gestionar su productividad, entretenimiento y aprendizaje desde una sola interfaz moderna y elegante.

---

## ✨ Características Principales

### 🤖 Chat IA
- Asistente inteligente integrado con múltiples proveedores (OpenAI, Groq, Ollama)
- Respuestas en tiempo real con contexto personalizado
- Interfaz moderna tipo chat con historial de conversaciones
- Soporte para imágenes y análisis visual
- Respuestas empáticas y sentimentales

### 🎵 Música
- Reproductor musical interactivo con YouTube
- Sistema de playlists personalizadas
- Favoritos y gestión de biblioteca
- Búsqueda de letras y sincronización
- Estadísticas de reproducción

### 🎮 Juegos
- Módulo de entretenimiento con minijuegos educativos
- Sistema de puntuaciones y logros
- Interfaz dinámica y visual
- Desafíos diarios y rankings

### 🌦️ Clima
- Consulta del clima en tiempo real
- Información de temperatura, humedad y condiciones meteorológicas
- Diseño con animaciones fluidas
- Geolocalización automática
- Pronóstico extendido

### 🌍 Traductor
- Traducción entre múltiples idiomas
- Interfaz rápida y sencilla
- Detección automática de idioma
- Historial de traducciones

### 🎬 Entretenimiento
- Sección de contenido multimedia
- Tendencias y categorías interactivas
- Recomendaciones personalizadas
- Películas, series, anime y más

### 📝 Blog / Noticias Globales
- Publicaciones personales de usuarios
- Noticias oficiales creadas por administradores
- Sistema de anuncios globales
- Publicaciones fijadas y destacadas
- Categorías y comentarios

### 📅 Eventos
- Gestión y visualización de eventos
- Organización de actividades
- Sistema de recordatorios
- Calendario interactivo
- Sincronización con notificaciones

### 🔔 Notificaciones
- Centro de notificaciones moderno con diseño tipo app
- Agrupación por fecha (Hoy, Ayer, Esta semana, Este mes)
- Sección de notificaciones destacadas para prioridad alta
- Buscador en tiempo real
- Filtros por categoría (Chat IA, Música, Estudio, Eventos, etc.)
- Acciones rápidas: marcar leída, fijar, eliminar
- Estadísticas visuales por categoría
- Colores e iconos específicos por tipo de notificación
- Prioridades: Alta (🔥), Normal, Baja (📌)
- Sistema de fijación para notificaciones importantes

### 👤 Perfil de Usuario
- Gestión de perfil completo
- Personalización de cuenta
- Configuración de tema (claro/oscuro)
- Foto de perfil
- Estadísticas de uso

### 🛠 Soporte Técnico
- Sistema de tickets avanzado
- Comunicación entre usuarios y administradores
- Seguimiento de incidencias
- Respuesta por correo electrónico
- Estadísticas de tiempos de respuesta

### 💡 Sugerencias
- Envío de sugerencias por parte de usuarios
- Revisión y respuesta administrativa
- Sistema de votación
- Estado de implementación

### 📊 Panel de Administración
- Dashboard con métricas en tiempo real
- Gestión de usuarios y permisos
- Exportación de reportes en Excel con diagramas
- Estadísticas detalladas de todas las secciones
- Gestión de contenido global

---

## 🏗 Tecnologías Utilizadas

### Backend
<div align="center">

![Python](https://img.shields.io/badge/Python-3.14-blue.svg)
![Django](https://img.shields.io/badge/Django-6.0.6-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightblue.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-6.0-green.svg)
![Redis](https://img.shields.io/badge/Redis-7.0-red.svg)

</div>

- **Python 3.14** - Lenguaje principal
- **Django 6.0.6** - Framework web
- **SQLite** - Usuarios, Auth, Sesiones
- **MongoDB** - Chats, Notificaciones, Analítica
- **Redis** - Caché, Sesiones, Colas

### Frontend
<div align="center">

![HTML5](https://img.shields.io/badge/HTML5-E34F26.svg)
![CSS3](https://img.shields.io/badge/CSS3-1572B6.svg)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E.svg)
![Glassmorphism](https://img.shields.io/badge/Glassmorphism-UI-purple.svg)

</div>

- **HTML5** - Estructura semántica
- **CSS3** - Estilos avanzados con Glassmorphism
- **JavaScript** - Interactividad y animaciones
- **Glassmorphism UI** - Diseño moderno con efectos de vidrio

### APIs y Servicios
<div align="center">

![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-black.svg)
![Groq](https://img.shields.io/badge/Groq-Llama--3-orange.svg)
![OpenWeather](https://img.shields.io/badge/OpenWeather-API-blue.svg)
![DeepTranslator](https://img.shields.io/badge/DeepTranslator-API-green.svg)

</div>

- **OpenAI API** - GPT-4o para Chat IA
- **Groq API** - Llama 3.3 para respuestas rápidas
- **Open-Meteo API** - Datos del clima
- **Deep Translator** - Traducción multilenguaje

---

## 📁 Estructura del Proyecto

```bash
MiniAmigixV/
│
├── apps/
│   ├── api/              # API REST con Django REST Framework
│   ├── app/              # Aplicación principal (Chat, Música, Juegos)
│   ├── blog/             # Blog y noticias globales
│   ├── clima/            # Clima en tiempo real
│   ├── configuracion/    # Configuración de usuario
│   ├── estudio/          # Recursos de estudio y Pomodoro
│   ├── eventos/          # Gestión de eventos y agenda
│   ├── mongodb/          # Modelos y servicios MongoDB
│   ├── notificaciones/    # Sistema de notificaciones avanzado
│   ├── perfil/           # Perfil de usuario
│   ├── soporte/          # Sistema de soporte técnico
│   ├── sugerencias/      # Sistema de sugerencias
│   ├── traductor/        # Traductor multilenguaje
│   └── tutorial/         # Tutorial y guía interactiva
│
├── static/
│   ├── css/
│   │   ├── core/         # Estilos base y variables
│   │   ├── modules/      # Estilos por módulo
│   │   └── pages/        # Estilos por página
│   ├── js/
│   │   ├── core/         # JavaScript base
│   │   ├── modules/      # JavaScript por módulo
│   │   └── pages/        # JavaScript por página
│   ├── imagenes/         # Imágenes y logos
│   └── fonts/            # Fuentes personalizadas
│
├── templates/
│   ├── account/         # Plantillas de cuenta (login, registro)
│   ├── blog/            # Plantillas del blog
│   ├── clima/           # Plantillas del clima
│   ├── configuracion/   # Plantillas de configuración
│   ├── estudio/         # Plantillas de estudio
│   ├── eventos/         # Plantillas de eventos
│   ├── includes/        # Componentes reutilizables
│   ├── notificaciones/  # Plantillas de notificaciones
│   ├── perfil/          # Plantillas de perfil
│   ├── soporte/         # Plantillas de soporte
│   └── traductor/       # Plantillas del traductor
│
├── config/               # Configuración de Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── media/               # Archivos multimedia subidos
├── scripts/             # Scripts utilitarios
├── scratch/             # Archivos temporales de desarrollo
├── .github/             # Configuración de GitHub
├── .venv/               # Entorno virtual
├── venv/                # Entorno virtual alternativo
├── db.sqlite3           # Base de datos SQLite
├── manage.py            # Script de gestión Django
├── requirements.txt     # Dependencias Python
└── README.md           # Documentación del proyecto
```

---

## ⚙ Instalación

### Requisitos Previos
- Python 3.14 o superior
- pip (gestor de paquetes de Python)
- Git

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/maria45889/MiniAmigixV.git
cd MiniAmigixV
```

### Paso 2: Crear Entorno Virtual

```bash
python -m venv venv
```

### Paso 3: Activar Entorno Virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / Mac:**
```bash
source venv/bin/activate
```

### Paso 4: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 5: Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu_clave_secreta_de_django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MongoDB
MONGODB_URI=mongodb://localhost:27017/miniamigixv_db

# Redis
REDIS_URL=redis://localhost:6379/0

# APIs de IA
OPENAI_API_KEY=tu_api_key_de_openai
GROQ_API_KEY=tu_api_key_de_groq

# Correo (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña
```

### Paso 6: Aplicar Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### Paso 7: Crear Superusuario

```bash
python manage.py createsuperuser
```

### Paso 8: Ejecutar Servidor

```bash
python manage.py runserver
```

### Paso 9: Acceder a la Aplicación

Abre tu navegador y navega a:
- **Aplicación:** http://127.0.0.1:8000/
- **Panel Admin:** http://127.0.0.1:8000/admin/
- **Panel de Administración:** http://127.0.0.1:8000/panel-admin/

---

## 🔐 Roles del Sistema

### 👤 Usuario Normal

**Permisos:**
- ✅ Usar Chat IA
- ✅ Crear publicaciones en el blog
- ✅ Ver noticias globales
- ✅ Crear tickets de soporte
- ✅ Enviar sugerencias
- ✅ Gestionar eventos personales
- ✅ Usar reproductor de música
- ✅ Jugar minijuegos
- ✅ Consultar el clima
- ✅ Usar el traductor
- ✅ Acceder a recursos de estudio

### 👨‍💼 Administrador

**Permisos Adicionales:**
- ✅ Publicar noticias oficiales
- ✅ Fijar anuncios globales
- ✅ Responder tickets de soporte
- ✅ Gestionar sugerencias
- ✅ Acceder al panel de administración
- ✅ Exportar reportes en Excel
- ✅ Gestionar usuarios
- ✅ Responder por correo a usuarios
- ✅ Ver estadísticas detalladas
- ✅ Configurar el sistema

---

## 🔔 Cambios Recientes

### 🆕 Última Actualización - Exportación de Reportes Excel

**Commit:** `cf0b2cf`

**Novedades:**
- ✨ Nuevo endpoint para exportar reportes en Excel con diagramas
- 📊 5 hojas con métricas detalladas: Resumen General, Usuarios, Soporte, Visitantes, Música
- 📈 Gráficos de barras y pie en todas las hojas
- 🎨 Diseño profesional con estilos y bordes
- 📥 Descarga automática al hacer clic en "Ver reportes"
- 🔒 Solo accesible para administradores autorizados

**Archivos Modificados:**
- `apps/app/views.py` - Función `exportar_reporte_excel`
- `apps/app/urls.py` - Ruta `/panel-admin/exportar-excel/`
- `templates/panel_admin.html` - Botón de descarga
- `requirements.txt` - Dependencias `openpyxl` y `xlsxwriter`

---

### 🎨 Actualización Anterior - Centro de Notificaciones

**Commit:** `979c665`

**Novedades:**
- Modernización completa del centro de notificaciones con diseño tipo app
- Agrupación por fecha (Hoy, Ayer, Esta semana, Este mes)
- Sección de notificaciones destacadas para prioridad alta
- Buscador en tiempo real con filtrado por título y mensaje
- Filtros por categoría (Chat IA, Música, Estudio, Eventos, Soporte, Sistema, etc.)
- Botones de acción: marcar leída, fijar, eliminar individualmente
- Estadísticas visuales por categoría con iconos específicos
- Header moderno con badges de contadores (sin leer, total)
- Colores e iconos específicos por tipo de notificación
- Sistema de prioridades: Alta (🔥), Normal, Baja (📌)
- Sistema de fijación para notificaciones importantes
- Animaciones y transiciones suaves
- Diseño responsivo optimizado para móviles

---

### 📧 Actualización - Respuesta por Correo

**Commit:** `e6922c7`

**Novedades:**
- Funcionalidad para que el administrador principal pueda responder por correo a usuarios
- Ruta: `panel-admin/user-email/<int:user_id>/`
- Plantillas HTML personalizadas para correos
- Integración con EmailMultiAlternatives

> **Nota:** Requiere configurar credenciales SMTP en `config/settings.py`

---

## 🎨 Diseño UI/UX

MiniAmigixV utiliza una interfaz visual moderna basada en:

<div align="center">

**Glassmorphism** • **Degradados Neon** • **Animaciones Suaves** • **Responsive Design** • **Dashboard Experience**

</div>

### Inspiración Visual
- 🎬 Netflix - Interfaz de contenido multimedia
- 🎵 Spotify - Reproductor de música y playlists
- 📊 Dashboards futuristas - Visualización de datos
- 🌟 Apple Design - Minimalismo y elegancia

### Características de Diseño
- Efectos de vidrio esmerilado (glassmorphism)
- Gradientes vibrantes y modernos
- Transiciones fluidas y naturales
- Tipografía clara y legible
- Iconos intuitivos y consistentes
- Paleta de colores cohesiva
- Modo oscuro/claro (en desarrollo)

---

## 🚀 Futuras Mejoras

### 📋 Roadmap

- [ ] **Notificaciones Push** - Sistema de alertas en tiempo real
- [ ] **Modo Oscuro Avanzado** - Toggle completo con persistencia
- [ ] **Dashboard Analítico** - Estadísticas detalladas para usuarios
- [ ] **Más Minijuegos** - Ampliar catálogo de juegos educativos
- [ ] **IA Más Avanzada** - Integración con más modelos y features
- [ ] **Sistema de Recomendaciones** - Personalización basada en uso
- [ ] **App Móvil Android** - Versión nativa para Android
- [ ] **Integración con Calendarios** - Google Calendar, Outlook
- [ ] **Sistema de Gamificación** - Puntos, niveles y recompensas
- [ ] **Chat de Grupos** - Conversaciones colaborativas
- [ ] **Videoconferencias** - Integración con plataformas de video
- [ ] **Almacenamiento en la Nube** - Google Drive, Dropbox

---

## 📊 Estadísticas del Proyecto

<div align="center">

![GitHub Stars](https://img.shields.io/github/stars/maria45889/MiniAmigixV?style=social)
![GitHub Forks](https://img.shields.io/github/forks/maria45889/MiniAmigixV?style=social)
![GitHub Issues](https://img.shields.io/github/issues/maria45889/MiniAmigixV)
![GitHub License](https://img.shields.io/github/license/maria45889/MiniAmigixV)

</div>

### Lenguajes del Proyecto

<div align="center">

![HTML](https://img.shields.io/badge/HTML-52.2%25-orange.svg)
![CSS](https://img.shields.io/badge/CSS-32.2%25-blue.svg)
![Python](https://img.shields.io/badge/Python-11.6%25-green.svg)
![JavaScript](https://img.shields.io/badge/JavaScript-3.8%25-yellow.svg)
![Other](https://img.shields.io/badge/Other-0.2%25-gray.svg)

</div>

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Si deseas contribuir a MiniAmigixV, por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guía de Contribución
- Respeta el estilo de código existente
- Escribe tests para nuevas features
- Actualiza la documentación
- Sé respetuoso y constructivo

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👩‍💻 Autor

<div align="center">

### María José Taco

[![GitHub](https://img.shields.io/badge/Github-maria45889-black.svg)](https://github.com/maria45889)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-María--José--Taco-blue.svg)](https://linkedin.com/in/maria-jose-taco)

**Desarrolladora Web Full Stack**

Especialista en Django, Python y desarrollo de interfaces modernas. Apasionada por crear experiencias digitales únicas y funcionales.

</div>

---

## 🙏 Agradecimientos

- A toda la comunidad de Django por su increíble framework
- A los creadores de las APIs de IA que hacen posible este proyecto
- A todos los usuarios que prueban y mejoran MiniAmigixV

---

## 📞 Soporte

¿Tienes preguntas o sugerencias?

- 📧 Email: miniamigixv@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/maria45889/MiniAmigixV/issues)
- 💬 Discord: [Únete a nuestro servidor](#)

---

<div align="center">

**⭐ Si te gusta este proyecto, ¡dale una estrella en GitHub! ⭐**

Made with ❤️ by María José Taco

</div>
