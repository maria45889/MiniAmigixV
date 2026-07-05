# MiniAmigixV 🚀

MiniAmigixV es una aplicación web moderna desarrollada con **Django** que integra múltiples herramientas inteligentes en una sola plataforma, ofreciendo una experiencia visual premium con diseño **glassmorphism**, interfaz responsiva y funcionalidades potenciadas por IA.

## ✨ Características Principales

### 🤖 Chat IA

* Asistente inteligente integrado.
* Respuestas en tiempo real.
* Interfaz moderna tipo chat.

### 🎵 Música

* Reproductor musical interactivo.
* Experiencia multimedia integrada.

### 🎮 Juegos

* Módulo de entretenimiento con minijuegos.
* Interfaz dinámica y visual.

### 🌦 Clima

* Consulta del clima en tiempo real.
* Información de temperatura, humedad y condiciones meteorológicas.
* Diseño premium con animaciones.

### 🌍 Traductor

* Traducción entre múltiples idiomas.
* Interfaz rápida y sencilla.

### 🎬 Entretenimiento

* Sección de contenido multimedia.
* Tendencias y categorías interactivas.

### 📝 Blog / Noticias Globales

* Publicaciones personales de usuarios.
* Noticias oficiales creadas por administradores.
* Sistema de anuncios globales.
* Publicaciones fijadas y destacadas.

### 📅 Eventos

* Gestión y visualización de eventos.
* Organización de actividades.

### 🔔 Notificaciones

* Centro de notificaciones moderno con diseño premium.
* Agrupación por fecha (Hoy, Ayer, Esta semana, Este mes).
* Sección de notificaciones destacadas para prioridad alta.
* Buscador en tiempo real.
* Filtros por categoría (Chat IA, Música, Estudio, Eventos, etc.).
* Acciones rápidas: marcar leída, fijar, eliminar.
* Estadísticas visuales por categoría.
* Colores e iconos específicos por tipo de notificación.
* Prioridades: Alta, Normal, Baja.
* Sistema de fijación para notificaciones importantes.

### 👤 Perfil de Usuario

* Gestión de perfil.
* Personalización de cuenta.

### 🛠 Soporte Técnico

* Sistema de tickets.
* Comunicación entre usuarios y administradores.
* Seguimiento de incidencias.

### 💡 Sugerencias

* Envío de sugerencias por parte de usuarios.
* Revisión y respuesta administrativa.

---

# 🏗 Tecnologías Utilizadas

## Backend

* Python 3
* Django
* SQLite (Usuarios, Auth, Sesiones)
* MongoDB (Chats, Notificaciones, Analítica)
* Redis (Caché, Sesiones, Colas)

## Frontend

* HTML5
* CSS3
* JavaScript
* Glassmorphism UI

## APIs y Servicios

* APIs de IA
* APIs de clima
* APIs de traducción

---

# 🚀 Futuras Mejoras

* Notificaciones push — sistema de alertas en tiempo real para avisos, mensajes y novedades importantes.
* Modo oscuro avanzado
* Dashboard analítico
* Más minijuegos
* IA más avanzada

---

# 📁 Estructura del Proyecto

```bash
MiniAmigixV/
│
├── apps/
│   ├── api/              # API REST
│   ├── app/              # Aplicación principal
│   ├── blog/             # Blog y noticias
│   ├── clima/            # Clima en tiempo real
│   ├── configuracion/    # Configuración de usuario
│   ├── estudio/          # Recursos de estudio y Pomodoro
│   ├── eventos/          # Gestión de eventos
│   ├── mongodb/          # Modelos MongoDB
│   ├── notificaciones/    # Sistema de notificaciones
│   ├── perfil/           # Perfil de usuario
│   ├── soporte/          # Sistema de soporte técnico
│   ├── sugerencias/      # Sistema de sugerencias
│   ├── traductor/        # Traductor multilenguaje
│   └── tutorial/         # Tutorial y guía
│
├── static/
│   ├── css/
│   │   ├── core/         # Estilos base
│   │   ├── modules/      # Estilos por módulo
│   │   └── pages/        # Estilos por página
│   ├── js/
│   ├── imagenes/         # Imágenes y logos
│   └── fonts/            # Fuentes personalizadas
│
├── templates/
│   ├── account/         # Plantillas de cuenta
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

# ⚙ Instalación

## 1. Clonar repositorio

```bash
git clone https://github.com/maria45889/MiniAmigixV.git
```

## 2. Entrar al proyecto

```bash
cd MiniAmigixV
```

## 3. Crear entorno virtual

```bash
python -m venv venv
```

## 4. Activar entorno virtual

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

## 5. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 6. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

## 7. Ejecutar servidor

```bash
python manage.py runserver
```

---

# 🔐 Roles del Sistema

## Usuario Normal

Puede:

* Usar chat IA
* Crear publicaciones
* Ver noticias globales
* Crear tickets de soporte
* Enviar sugerencias

## Administrador

Puede además:

* Publicar noticias oficiales
* Fijar anuncios globales
* Responder tickets
* Gestionar sugerencias
* Acceder al panel admin

---

# 🔔 Cambios recientes

## Última Actualización - Centro de Notificaciones Premium

- Modernización completa del centro de notificaciones con diseño premium tipo app.
- Añadidos campos de prioridad, categoría y fijación al modelo Notificacion.
- Implementación de agrupación por fecha (Hoy, Ayer, Esta semana, Este mes).
- Sección de notificaciones destacadas para prioridad alta.
- Buscador en tiempo real con filtrado por título y mensaje.
- Filtros por categoría (Chat IA, Música, Estudio, Eventos, Soporte, Sistema, etc.).
- Botones de acción: marcar leída, fijar, eliminar individualmente.
- Estadísticas visuales por categoría con iconos específicos.
- Header moderno con badges de contadores (sin leer, total).
- Colores e iconos específicos por tipo de notificación.
- Sistema de prioridades: Alta (🔥), Normal, Baja (📌).
- Sistema de fijación para notificaciones importantes.
- Animaciones y transiciones suaves.
- Diseño responsivo optimizado para móviles.
- Commit: `979c665` (Modernizar centro de notificaciones con diseño premium).

## Actualización Anterior - Respuesta por Correo

- Se añadió la funcionalidad para que el administrador principal (`miniamigixv@gmail.com`) pueda responder por correo a usuarios directamente desde el panel de administración.
- Rutas y plantillas relevantes:
  - `apps/app/urls.py`: `panel-admin/user-email/<int:user_id>/`
  - Plantilla del formulario: `templates/panel_admin_email_user.html`
  - Plantilla del email HTML: `templates/email_admin_response.html`
- Commit con este cambio: `e6922c7` (Añadir respuesta por correo en panel admin, plantilla y mejoras de UI).

> Nota: El envío usa `EmailMultiAlternatives` y requiere configurar las credenciales SMTP en `config/settings.py` (ver sección "Configuración de correo").


# 🎨 Diseño UI/UX

MiniAmigixV utiliza una interfaz visual moderna basada en:

* Glassmorphism
* Degradados neon
* Animaciones suaves
* Responsive Design
* Experiencia tipo dashboard premium

Inspiración visual:

* Netflix
* Spotify
* Dashboards futuristas

---

# 🚀 Futuras Mejoras

* Notificaciones push
* Modo oscuro avanzado
* Dashboard analítico
* Más minijuegos
* IA más avanzada
* Sistema de recomendaciones

---

# 👩‍💻 Autor

Desarrollado por **María José Taco**

GitHub:
https://github.com/maria45889
