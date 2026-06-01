# MiniAmigixV

MiniAmigixV es una aplicación web integral creada con Django. Reúne herramientas de productividad, entretenimiento y asistencia inteligente en una sola plataforma: chat con IA, eventos, música, clima, juegos, estudios, blog, traductor, notificaciones, configuración, autenticación, perfil de usuario, modo claro/oscuro y más.

## Vista General

El objetivo de MiniAmigixV es ofrecer una experiencia web amigable, moderna y organizada, con módulos independientes que puedan crecer de forma escalable dentro del proyecto.

## Características

- Interfaz moderna y responsive.
- Modo claro y modo oscuro.
- Login, registro y perfil de usuario.
- Chat IA integrado.
- Gestión de eventos.
- Reproductor de música.
- Consulta de clima.
- Juegos integrados.
- Recursos de estudio.
- Traductor multiidioma.
- Blog y contenido informativo.
- Sistema de notificaciones.
- Configuración personalizada.
- Reloj en tiempo real.
- Sugerencias y tutoriales.
- Arquitectura modular con Django Apps.

## Estructura Del Proyecto

```plaintext
miniamigixv/
├── apps/
│   ├── users/
│   ├── chat/
│   ├── musica/
│   ├── clima/
│   ├── eventos/
│   ├── juegos/
│   ├── estudios/
│   ├── blog_app/
│   ├── notificaciones/
│   └── traductor/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
│   ├── css/
│   └── js/
├── templates/
│   ├── base.html
│   └── home.html
├── manage.py
└── db.sqlite3
```

## Tecnologías

- Python
- Django
- HTML5
- CSS3
- JavaScript
- SQLite3
- Git
- GitHub

## Instalación

Clona el repositorio:

```bash
git clone https://github.com/maria45889/MiniAmigixV.git
```

Entra al proyecto:

```bash
cd MiniAmigixV
```

Crea un entorno virtual:

```bash
python -m venv env
```

Activa el entorno virtual en Windows:

```bash
env\Scripts\activate
```

Instala las dependencias:

```bash
pip install django
```

Ejecuta las migraciones:

```bash
python manage.py migrate
```

Inicia el servidor de desarrollo:

```bash
python manage.py runserver
```

Abre la aplicación en el navegador:

```plaintext
http://127.0.0.1:8000/
```

## Uso

Después de iniciar el servidor, puedes navegar por los módulos principales desde la interfaz de MiniAmigixV:

- Inicio
- Chat IA
- Música
- Eventos
- Estudios
- Clima
- Juegos
- Blog
- Traductor
- Notificaciones
- Configuración

## Comandos Útiles

Ver el estado del repositorio:

```bash
git status
```

Cambiar a la rama principal:

```bash
git checkout main
```

Actualizar la rama principal:

```bash
git pull origin main
```

Subir cambios a GitHub:

```bash
git add README.md
git commit -m "Actualizar README del proyecto"
git push origin main
```

## Contribuciones

Las contribuciones son bienvenidas. Para proponer una mejora:

1. Haz fork del proyecto.
2. Crea una nueva rama.
3. Realiza tus cambios.
4. Haz commit con un mensaje claro.
5. Sube la rama a GitHub.
6. Abre un Pull Request.

```bash
git checkout -b feature/nueva-funcionalidad
git add .
git commit -m "Agregar nueva funcionalidad"
git push origin feature/nueva-funcionalidad
```

## Licencia

Proyecto desarrollado con cariño por **Maria Jose Taco Calle**.

## Contacto

**MiniAmigixV**  
Tu plataforma inteligente todo en uno.
