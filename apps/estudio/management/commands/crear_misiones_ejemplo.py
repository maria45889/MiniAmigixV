from django.core.management.base import BaseCommand
from apps.estudio.models import Mision

class Command(BaseCommand):
    help = 'Crear misiones de ejemplo para Mundo Amigis'

    def handle(self, *args, **options):
        misiones_ejemplo = [
            {
                'titulo': '🪙 ¿A dónde se va tu dinero?',
                'descripcion': 'Tienes $100 este mes. ¿Cómo los distribuirías entre necesidades, comida, entretenimiento y ahorro?',
                'categoria': 'vida',
                'xp_recompensa': 50,
                'monedas_recompensa': 20,
                'dificultad': 'facil',
                'contenido_interactivo': {
                    'pregunta': 'Tienes $100 este mes. ¿Cómo los distribuirías?',
                    'opciones': [
                        {'texto': '🏠 Necesidades $50, 🍔 Comida $20, 🎮 Entretenimiento $15, 💰 Ahorro $15', 'correcta': True},
                        {'texto': '🏠 Necesidades $20, 🍔 Comida $50, 🎮 Entretenimiento $25, 💰 Ahorro $5', 'correcta': False},
                        {'texto': '🏠 Necesidades $10, 🍔 Comida $20, 🎮 Entretenimiento $60, 💰 Ahorro $10', 'correcta': False}
                    ],
                    'explicacion': 'La distribución equilibrada es clave para el manejo financiero. Las necesidades deben tener prioridad, pero el ahorro es importante.'
                }
            },
            {
                'titulo': '🧠 ¿Por qué tenemos déjà vu?',
                'descripcion': 'Descubre la ciencia detrás de esa sensación de haber vivido algo antes.',
                'categoria': 'curiosidad',
                'xp_recompensa': 40,
                'monedas_recompensa': 15,
                'dificultad': 'facil',
                'contenido_interactivo': {
                    'pregunta': '¿Qué es el déjà vu?',
                    'opciones': [
                        {'texto': 'Un error en el procesamiento de memoria del cerebro', 'correcta': True},
                        {'texto': 'Una visión del futuro', 'correcta': False},
                        {'texto': 'Un recuerdo de una vida pasada', 'correcta': False}
                    ],
                    'explicacion': 'El déjà vu es un fenómeno donde el cerebro "confunde" el presente con el pasado, creando una sensación de familiaridad.'
                }
            },
            {
                'titulo': '🍳 Cómo hacer un huevo perfecto',
                'descripcion': 'Aprende la técnica exacta para cocinar un huevo en el punto exacto.',
                'categoria': 'practico',
                'xp_recompensa': 35,
                'monedas_recompensa': 15,
                'dificultad': 'facil',
                'contenido_interactivo': {
                    'pregunta': '¿Cuántos minutos necesita un huevo para estar cocido pero con yema líquida?',
                    'opciones': [
                        {'texto': '3-4 minutos', 'correcta': True},
                        {'texto': '8-10 minutos', 'correcta': False},
                        {'texto': '15 minutos', 'correcta': False}
                    ],
                    'explicacion': 'Para un huevo con yema líquida, 3-4 minutos es perfecto. El tiempo exacto depende del tamaño del huevo.'
                }
            },
            {
                'titulo': '🎨 ¿Por qué algunos colores combinan mejor?',
                'descripcion': 'Descubre la teoría del color y cómo crear combinaciones armoniosas.',
                'categoria': 'creativo',
                'xp_recompensa': 45,
                'monedas_recompensa': 18,
                'dificultad': 'medio',
                'contenido_interactivo': {
                    'pregunta': '¿Qué colores son complementarios?',
                    'opciones': [
                        {'texto': 'Azul y naranja', 'correcta': True},
                        {'texto': 'Rojo y verde', 'correcta': True},
                        {'texto': 'Azul y verde', 'correcta': False}
                    ],
                    'explicacion': 'Los colores complementarios están opuestos en la rueda de color y crean contraste visual fuerte.'
                }
            },
            {
                'titulo': '🌎 ¿Por qué existen los husos horarios?',
                'descripcion': 'Entiende cómo la rotación de la Tierra afecta el tiempo global.',
                'categoria': 'mundo',
                'xp_recompensa': 40,
                'monedas_recompensa': 16,
                'dificultad': 'facil',
                'contenido_interactivo': {
                    'pregunta': '¿Por qué tenemos diferentes husos horarios?',
                    'opciones': [
                        {'texto': 'Porque la Tierra rota y el sol no ilumina todo al mismo tiempo', 'correcta': True},
                        {'texto': 'Porque cada país quiere su propio horario', 'correcta': False},
                        {'texto': 'Porque la Luna afecta el tiempo', 'correcta': False}
                    ],
                    'explicacion': 'La Tierra rota 360° en 24 horas, creando 24 husos horarios de 15° cada uno.'
                }
            },
            {
                'titulo': '🗣️ Cómo hablar en público sin nervios',
                'descripcion': 'Técnicas para mejorar tu comunicación y confianza.',
                'categoria': 'habilidades',
                'xp_recompensa': 55,
                'monedas_recompensa': 22,
                'dificultad': 'medio',
                'contenido_interactivo': {
                    'pregunta': '¿Qué técnica ayuda a reducir los nervios al hablar en público?',
                    'opciones': [
                        {'texto': 'Practicar respiración profunda', 'correcta': True},
                        {'texto': 'Hablar muy rápido para terminar pronto', 'correcta': False},
                        {'texto': 'No prepararse nada', 'correcta': False}
                    ],
                    'explicacion': 'La respiración profunda ayuda a calmar el sistema nervioso y reduce la ansiedad.'
                }
            }
        ]

        creadas = 0
        for mision_data in misiones_ejemplo:
            if not Mision.objects.filter(titulo=mision_data['titulo']).exists():
                Mision.objects.create(**mision_data)
                creadas += 1
                self.stdout.write(self.style.SUCCESS(f'Misión creada: {mision_data["titulo"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Misión ya existe: {mision_data["titulo"]}'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Se crearon {creadas} misiones de ejemplo.'))
