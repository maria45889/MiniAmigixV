from django.core.management.base import BaseCommand
from apps.juegos.models import Game, Achievement


class Command(BaseCommand):
    help = 'Populate the database with initial games and achievements'

    def handle(self, *args, **options):
        # Create initial games
        games_data = [
            {
                'nombre': 'Tres en Raya',
                'descripcion': 'Desafía a Amigis en el clásico Tic-Tac-Toe y demuestra tu estrategia.',
                'categoria': 'clasico',
                'icono': '❌⭕'
            },
            {
                'nombre': 'Snake Arcade',
                'descripcion': 'Guía a la serpiente para comer las manzanas sin chocar con los bordes.',
                'categoria': 'arcade',
                'icono': '🐍'
            },
            {
                'nombre': 'Juego de Memoria',
                'descripcion': 'Encuentra los pares de cartas idénticas en el menor tiempo posible.',
                'categoria': 'clasico',
                'icono': '🧠'
            },
            {
                'nombre': 'Adivina el Número',
                'descripcion': 'Descubre el número secreto del 1 al 100 con pistas de Amigis.',
                'categoria': 'clasico',
                'icono': '🎯'
            },
            {
                'nombre': 'Sudoku Challenge',
                'descripcion': 'Ejercita tu mente resolviendo tableros numéricos de lógica pura.',
                'categoria': 'educativo',
                'icono': '🧮'
            },
            {
                'nombre': 'Rompecabezas',
                'descripcion': 'Arma la imagen deslizante de Amigis en pocas jugadas.',
                'categoria': 'clasico',
                'icono': '🧩'
            },
            {
                'nombre': 'Adivina el Animal',
                'descripcion': 'Amigis te dará pistas sobre un animal del reino salvaje. ¿Podrás adivinarlo?',
                'categoria': 'ia',
                'icono': '🦆'
            },
            {
                'nombre': 'Trivia Educativa',
                'descripcion': 'Preguntas y respuestas sobre ciencia, historia y cultura general.',
                'categoria': 'educativo',
                'icono': '❓'
            },
            {
                'nombre': 'Capitales del Mundo',
                'descripcion': 'Demuestra tus conocimientos de geografía adivinando las capitales globales.',
                'categoria': 'educativo',
                'icono': '🌍'
            },
            {
                'nombre': 'Retos de Programación',
                'descripcion': 'Desafíos rápidos de código en Python, JavaScript y algoritmos.',
                'categoria': 'educativo',
                'icono': '💻'
            },
            {
                'nombre': 'Adivina el Personaje',
                'descripcion': 'Responde preguntas y deja que Amigis intente adivinar el personaje en tu mente.',
                'categoria': 'ia',
                'icono': '🎭'
            }
        ]

        for game_data in games_data:
            game, created = Game.objects.get_or_create(
                nombre=game_data['nombre'],
                defaults=game_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created game: {game.nombre}'))
            else:
                self.stdout.write(self.style.WARNING(f'Game already exists: {game.nombre}'))

        # Create initial achievements
        achievements_data = [
            {
                'nombre': 'Primera Victoria',
                'descripcion': 'Gana tu primer juego',
                'icono': '🏆',
                'puntos_xp': 50,
                'condicion': {'type': 'first_win'}
            },
            {
                'nombre': 'Jugador Dedicado',
                'descripcion': 'Juega 10 partidas',
                'icono': '🎮',
                'puntos_xp': 100,
                'condicion': {'type': 'games_played', 'count': 10}
            },
            {
                'nombre': 'Maestro de la Memoria',
                'descripcion': 'Completa el juego de memoria en menos de 20 movimientos',
                'icono': '🧠',
                'puntos_xp': 150,
                'condicion': {'type': 'memory_master', 'moves': 20}
            },
            {
                'nombre': 'Serpiente Veloz',
                'descripcion': 'Alcanza una puntuación de 50 en Snake',
                'icono': '🐍',
                'puntos_xp': 200,
                'condicion': {'type': 'snake_score', 'score': 50}
            },
            {
                'nombre': 'Estratega Perfecto',
                'descripcion': 'Gana 3 partidas de Tres en Raya seguidas',
                'icono': '⭕',
                'puntos_xp': 150,
                'condicion': {'type': 'tic_tac_toe_streak', 'count': 3}
            },
            {
                'nombre': 'Racha de 7 Días',
                'descripcion': 'Juega durante 7 días consecutivos',
                'icono': '🔥',
                'puntos_xp': 300,
                'condicion': {'type': 'streak', 'days': 7}
            },
            {
                'nombre': 'Nivel 5',
                'descripcion': 'Alcanza el nivel 5',
                'icono': '⭐',
                'puntos_xp': 0,
                'condicion': {'type': 'level', 'level': 5}
            },
            {
                'nombre': 'Nivel 10',
                'descripcion': 'Alcanza el nivel 10',
                'icono': '🌟',
                'puntos_xp': 0,
                'condicion': {'type': 'level', 'level': 10}
            }
        ]

        for achievement_data in achievements_data:
            achievement, created = Achievement.objects.get_or_create(
                nombre=achievement_data['nombre'],
                defaults=achievement_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created achievement: {achievement.nombre}'))
            else:
                self.stdout.write(self.style.WARNING(f'Achievement already exists: {achievement.nombre}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated games and achievements'))
