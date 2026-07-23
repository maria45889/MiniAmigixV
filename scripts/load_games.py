import os
import sys
import django

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.app.models import Game

# Lista de 10 juegos para cargar
juegos_data = [
    {
        'nombre': 'Quiz Master',
        'descripcion': 'Pon a prueba tus conocimientos con preguntas de cultura general, ciencia, historia y más.',
        'tipo': 'quiz',
        'dificultad': 'medio',
        'categoria': 'inteligencia',
        'icono': '❓',
        'tiempo_estimado': '5 min'
    },
    {
        'nombre': 'Memoria Neón',
        'descripcion': 'Encuentra los pares de cartas idénticas en el menor tiempo posible.',
        'tipo': 'memoria',
        'dificultad': 'facil',
        'categoria': 'inteligencia',
        'icono': '🎯',
        'tiempo_estimado': '3 min'
    },
    {
        'nombre': 'Mente Rápida',
        'descripcion': 'Resuelve operaciones matemáticas contra el reloj.',
        'tipo': 'matematicas',
        'dificultad': 'medio',
        'categoria': 'velocidad',
        'icono': '🔢',
        'tiempo_estimado': '5 min'
    },
    {
        'nombre': 'Adivinanzas',
        'descripcion': 'Resuelve acertijos y adivinanzas para poner a prueba tu lógica.',
        'tipo': 'logica',
        'dificultad': 'facil',
        'categoria': 'inteligencia',
        'icono': '🧩',
        'tiempo_estimado': '3 min'
    },
    {
        'nombre': 'Reflejos',
        'descripcion': 'Mide tu tiempo de reacción haciendo clic en cuanto cambie el color.',
        'tipo': 'reflejos',
        'dificultad': 'facil',
        'categoria': 'velocidad',
        'icono': '⚡',
        'tiempo_estimado': '2 min'
    },
    {
        'nombre': 'Snake Neo',
        'descripcion': 'El clásico juego de la serpiente con un diseño moderno.',
        'tipo': 'snake',
        'dificultad': 'medio',
        'categoria': 'estrategia',
        'icono': '🐍',
        'tiempo_estimado': '5 min'
    },
    {
        'nombre': 'Fidget Spinner',
        'descripcion': 'Relájate girando el fidget virtual.',
        'tipo': 'fidget',
        'dificultad': 'facil',
        'categoria': 'relax',
        'icono': '🌀',
        'tiempo_estimado': '10 min'
    },
    {
        'nombre': 'Respiración',
        'descripcion': 'Sesión guiada de respiración para reducir el estrés.',
        'tipo': 'respiracion',
        'dificultad': 'facil',
        'categoria': 'relax',
        'icono': '🌬️',
        'tiempo_estimado': '5 min'
    },
    {
        'nombre': '3 en Raya',
        'descripcion': 'El clásico juego de tres en raya contra la IA.',
        'tipo': 'tres_en_raya',
        'dificultad': 'facil',
        'categoria': 'estrategia',
        'icono': 'X',
        'tiempo_estimado': '3 min'
    },
    {
        'nombre': 'Palabras',
        'descripcion': 'Forma palabras con las letras disponibles.',
        'tipo': 'palabras',
        'dificultad': 'medio',
        'categoria': 'inteligencia',
        'icono': '📝',
        'tiempo_estimado': '5 min'
    }
]

# Cargar juegos
for juego_data in juegos_data:
    juego, created = Game.objects.get_or_create(
        nombre=juego_data['nombre'],
        defaults={
            'descripcion': juego_data['descripcion'],
            'tipo': juego_data['tipo'],
            'dificultad': juego_data['dificultad'],
            'categoria': juego_data['categoria'],
            'icono': juego_data['icono'],
            'tiempo_estimado': juego_data['tiempo_estimado'],
            'activo': True
        }
    )
    if created:
        print(f"✓ Juego creado: {juego.nombre}")
    else:
        print(f"- Juego ya existe: {juego.nombre}")

print(f"\nTotal de juegos en base de datos: {Game.objects.count()}")
