import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tutorial.models import Category, Tutorial, Step
from django.contrib.auth.models import User

# Crear categorías
categories_data = [
    {
        'name': 'Introducción',
        'description': 'Conceptos básicos para comenzar a usar MiniAmigixV',
        'icon': 'book-open',
        'order': 1
    },
    {
        'name': 'Chat IA',
        'description': 'Aprende a usar el asistente de inteligencia artificial',
        'icon': 'message-square',
        'order': 2
    },
    {
        'name': 'Música',
        'description': 'Cómo usar el reproductor de música y crear playlists',
        'icon': 'music',
        'order': 3
    },
    {
        'name': 'Productividad',
        'description': 'Herramientas para mejorar tu productividad diaria',
        'icon': 'zap',
        'order': 4
    }
]

print("Creando categorías...")
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={
            'description': cat_data['description'],
            'icon': cat_data['icon'],
            'order': cat_data['order']
        }
    )
    if created:
        print(f"  ✓ Categoría creada: {category.name}")
    else:
        print(f"  - Categoría ya existe: {category.name}")

# Obtener usuario para asignar como creador
user = User.objects.first()
if not user:
    user = User.objects.create_user(username='admin', email='admin@example.com', password='admin123')
    print("  ✓ Usuario admin creado")

# Crear tutoriales
tutorials_data = [
    {
        'title': 'Bienvenido a MiniAmigixV',
        'description': 'Tutorial introductorio para conocer todas las funciones principales de la plataforma. Aprenderás a navegar, configurar tu perfil y usar las herramientas básicas.',
        'category': 'Introducción',
        'difficulty': 'beginner',
        'estimated_time': 15,
        'featured': True,
        'steps': [
            {'order': 1, 'title': 'Registro y Configuración', 'content': 'Regístrate con tu correo o redes sociales. Configura tu perfil y preferencias de tema.'},
            {'order': 2, 'title': 'Navegación Básica', 'content': 'Explora el menú principal y conoce cada sección de la plataforma.'},
            {'order': 3, 'title': 'Primeros Pasos', 'content': 'Realiza tu primera consulta al Chat IA y configura tu primera notificación.'}
        ]
    },
    {
        'title': 'Usando el Chat IA',
        'description': 'Domina el asistente de inteligencia artificial para obtener respuestas a tus preguntas, ayuda con tareas y mucho más.',
        'category': 'Chat IA',
        'difficulty': 'beginner',
        'estimated_time': 20,
        'featured': True,
        'steps': [
            {'order': 1, 'title': 'Interfaz del Chat', 'content': 'Conoce la interfaz del chat y sus funciones principales.'},
            {'order': 2, 'title': 'Formular Preguntas', 'content': 'Aprende a formular preguntas efectivas para obtener mejores respuestas.'},
            {'order': 3, 'title': 'Historial de Conversaciones', 'content': 'Gestiona tu historial de conversaciones y exporta tus chats.'}
        ]
    },
    {
        'title': 'Reproductor de Música',
        'description': 'Aprende a buscar, reproducir y organizar tu música favorita con nuestro reproductor integrado.',
        'category': 'Música',
        'difficulty': 'intermediate',
        'estimated_time': 25,
        'featured': False,
        'steps': [
            {'order': 1, 'title': 'Búsqueda de Música', 'content': 'Busca canciones por nombre, artista o álbum.'},
            {'order': 2, 'title': 'Control de Reproducción', 'content': 'Usa los controles de reproducción y ajusta el volumen.'},
            {'order': 3, 'title': 'Playlists', 'content': 'Crea y gestiona tus listas de reproducción personalizadas.'}
        ]
    },
    {
        'title': 'Gestión de Eventos',
        'description': 'Organiza tu agenda con el sistema de eventos y recordatorios de MiniAmigixV.',
        'category': 'Productividad',
        'difficulty': 'intermediate',
        'estimated_time': 30,
        'featured': False,
        'steps': [
            {'order': 1, 'title': 'Crear Eventos', 'content': 'Añade nuevos eventos a tu calendario personal.'},
            {'order': 2, 'title': 'Recordatorios', 'content': 'Configura recordatorios para no olvidar tus compromisos.'},
            {'order': 3, 'title': 'Vista de Calendario', 'content': 'Visualiza tus eventos en formato de calendario.'}
        ]
    }
]

print("\nCreando tutoriales...")
for tut_data in tutorials_data:
    category = Category.objects.get(name=tut_data['category'])
    tutorial, created = Tutorial.objects.get_or_create(
        title=tut_data['title'],
        defaults={
            'description': tut_data['description'],
            'category': category,
            'difficulty': tut_data['difficulty'],
            'estimated_time': tut_data['estimated_time'],
            'featured': tut_data['featured'],
            'created_by': user
        }
    )
    if created:
        print(f"  ✓ Tutorial creado: {tutorial.title}")
        # Crear pasos
        for step_data in tut_data['steps']:
            Step.objects.create(
                tutorial=tutorial,
                order=step_data['order'],
                title=step_data['title'],
                content=step_data['content']
            )
        print(f"    ✓ {len(tut_data['steps'])} pasos creados")
    else:
        print(f"  - Tutorial ya existe: {tutorial.title}")

print("\n✓ Datos de ejemplo creados exitosamente!")
print(f"Total categorías: {Category.objects.count()}")
print(f"Total tutoriales: {Tutorial.objects.count()}")
print(f"Total pasos: {Step.objects.count()}")
