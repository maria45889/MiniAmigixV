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

* Alertas y avisos importantes.
* Información en tiempo real.

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

### 🛡 Panel de Administración

* Acceso exclusivo para administradores.
* Gestión de:

  * Usuarios
  * Tickets
  * Sugerencias
  * Publicaciones
  * Noticias oficiales

---

# 🏗 Tecnologías Utilizadas

## Backend

* Python 3
* Django
* SQLite (desarrollo)

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

# 📂 Estructura del Proyecto

```bash
MiniAmigixV/
│
├── apps/
│   ├── app/
│   ├── soporte/
│   └── sugerencias/
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│
├── templates/
│
├── config/
│
├── db.sqlite3
└── manage.py
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
