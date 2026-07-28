# ============================================================================
# MANAGEMENT COMMAND - UPDATE TUTORIALS
# ============================================================================

from django.core.management.base import BaseCommand
from apps.tutorial.models import Category, Tutorial, Step, FAQ


class Command(BaseCommand):
    help = 'Actualizar tutoriales para que sean sobre cómo usar MiniAmigixV'

    def handle(self, *args, **options):
        self.stdout.write('Actualizando tutoriales de MiniAmigixV...')
        
        # Eliminar datos existentes
        Tutorial.objects.all().delete()
        Step.objects.all().delete()
        Category.objects.all().delete()
        FAQ.objects.all().delete()
        
        # Crear categorías sobre MiniAmigixV
        cat_inicio = Category.objects.create(
            name='Inicio',
            description='Aprende a usar el dashboard principal',
            icon='home',
            order=1
        )
        
        cat_chat = Category.objects.create(
            name='Chat IA',
            description='Aprende a usar el asistente inteligente',
            icon='message-square',
            order=2
        )
        
        cat_musica = Category.objects.create(
            name='Música',
            description='Aprende a gestionar tu música',
            icon='music',
            order=3
        )
        
        cat_perfil = Category.objects.create(
            name='Perfil',
            description='Personaliza tu cuenta',
            icon='user',
            order=4
        )
        
        # Crear tutoriales
        # Tutorial 1: Dashboard
        tut_dashboard = Tutorial.objects.create(
            title='Usar el Dashboard Principal',
            description='Aprende a navegar y usar todas las funciones del dashboard principal de MiniAmigixV.',
            category=cat_inicio,
            difficulty='beginner',
            estimated_time=10,
            featured=True
        )
        
        Step.objects.create(
            tutorial=tut_dashboard,
            order=1,
            title='Navegación Principal',
            content='El dashboard principal es tu centro de control. En la izquierda verás el menú de navegación con acceso rápido a todos los módulos: Chat IA, Música, Juegos, Estudio, Clima, Traductor, Blog, Eventos y más.'
        )
        
        Step.objects.create(
            tutorial=tut_dashboard,
            order=2,
            title='Estadísticas Personales',
            content='En la parte superior del dashboard verás tus estadísticas: canciones escuchadas, juegos jugados, eventos creados y más. Estas estadísticas se actualizan en tiempo real.'
        )
        
        Step.objects.create(
            tutorial=tut_dashboard,
            order=3,
            title='Accesos Rápidos',
            content='Los botones de acceso rápido te permiten ir directamente a las funciones más usadas sin tener que navegar por el menú lateral.'
        )
        
        # Tutorial 2: Chat IA
        tut_chat = Tutorial.objects.create(
            title='Usar el Chat IA',
            description='Aprende a conversar con MiniAmigix, nuestra inteligencia artificial amigable.',
            category=cat_chat,
            difficulty='beginner',
            estimated_time=15,
            featured=True
        )
        
        Step.objects.create(
            tutorial=tut_chat,
            order=1,
            title='Iniciar una Conversación',
            content='Entra al módulo Chat IA desde el menú lateral. Escribe tu pregunta o mensaje en el cuadro de texto y presiona Enter o el botón de enviar.'
        )
        
        Step.objects.create(
            tutorial=tut_chat,
            order=2,
            title='Tipos de Preguntas',
            content='Puedes preguntar sobre cualquier tema: ayuda con tareas, traducción, generación de ideas, explicación de conceptos, o simplemente conversar. Usa emojis para una mejor experiencia.'
        )
        
        Step.objects.create(
            tutorial=tut_chat,
            order=3,
            title='Historial de Conversaciones',
            content='Todas tus conversaciones se guardan automáticamente. Puedes ver tu historial en el panel lateral y continuar conversaciones anteriores.'
        )
        
        # Tutorial 3: Música
        tut_musica = Tutorial.objects.create(
            title='Gestionar Música',
            description='Aprende a buscar, reproducir y organizar tu música en MiniAmigixV.',
            category=cat_musica,
            difficulty='beginner',
            estimated_time=20
        )
        
        Step.objects.create(
            tutorial=tut_musica,
            order=1,
            title='Buscar Canciones',
            content='Usa la barra de búsqueda para encontrar canciones de YouTube. Puedes buscar por nombre, artista o álbum.'
        )
        
        Step.objects.create(
            tutorial=tut_musica,
            order=2,
            title='Reproducir Música',
            content='Haz clic en cualquier canción para reproducirla. El reproductor aparecerá en la parte inferior de la pantalla con controles de reproducción.'
        )
        
        Step.objects.create(
            tutorial=tut_musica,
            order=3,
            title='Crear Listas de Reproducción',
            content='Agrega canciones a tus favoritos y crea listas de reproducción personalizadas para organizar tu música según tus preferencias.'
        )
        
        # Tutorial 4: Perfil
        tut_perfil = Tutorial.objects.create(
            title='Personalizar tu Perfil',
            description='Aprende a configurar tu cuenta de MiniAmigixV a tu gusto.',
            category=cat_perfil,
            difficulty='beginner',
            estimated_time=10
        )
        
        Step.objects.create(
            tutorial=tut_perfil,
            order=1,
            title='Cambiar Avatar',
            content='Sube una imagen personalizada como tu avatar o selecciona uno de los avatares predeterminados disponibles.'
        )
        
        Step.objects.create(
            tutorial=tut_perfil,
            order=2,
            title='Editar Biografía',
            content='Escribe una breve descripción sobre ti que aparecerá en tu perfil público.'
        )
        
        Step.objects.create(
            tutorial=tut_perfil,
            order=3,
            title='Cambiar Tema',
            content='Selecciona entre modo claro y oscuro según tu preferencia. El tema se aplicará a toda la aplicación.'
        )
        
        Step.objects.create(
            tutorial=tut_perfil,
            order=4,
            title='Configurar Idioma',
            content='Elige el idioma en el que prefieres usar la aplicación. El idioma se aplicará a todos los textos de la interfaz.'
        )
        
        # Crear FAQs
        FAQ.objects.create(
            category=cat_inicio,
            question='¿Cómo navego entre módulos?',
            answer='Usa el menú lateral izquierdo para navegar entre los diferentes módulos de MiniAmigixV. Cada módulo tiene su propio ícono y nombre.',
            order=1
        )
        
        FAQ.objects.create(
            category=cat_chat,
            question='¿El Chat IA guarda mis conversaciones?',
            answer='Sí, todas tus conversaciones se guardan automáticamente en tu historial. Puedes verlas y continuarlas en cualquier momento desde el panel lateral del Chat IA.',
            order=1
        )
        
        FAQ.objects.create(
            category=cat_musica,
            question='¿De dónde proviene la música?',
            answer='La música se reproduce desde YouTube. Puedes buscar cualquier canción o video disponible en la plataforma.',
            order=1
        )
        
        FAQ.objects.create(
            category=cat_perfil,
            question='¿Puedo cambiar mi avatar?',
            answer='Sí, puedes subir tu propia imagen o seleccionar uno de los avatares predeterminados desde la sección de edición de perfil.',
            order=1
        )
        
        self.stdout.write(self.style.SUCCESS('✓ Tutoriales actualizados exitosamente'))
        self.stdout.write(f'  - Categorías creadas: {Category.objects.count()}')
        self.stdout.write(f'  - Tutoriales creados: {Tutorial.objects.count()}')
        self.stdout.write(f'  - Pasos creados: {Step.objects.count()}')
        self.stdout.write(f'  - FAQs creados: {FAQ.objects.count()}')
