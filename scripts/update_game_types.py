import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.app.models import Game

# Mapeo de nombres a tipos
mapeo_tipos = {
    'Quiz Master': 'quiz',
    'Memoria': 'memoria',
    'Mente Rápida': 'matematicas',
    'Adivinanza': 'logica',
    'Reflejos': 'reflejos',
    'Fidget': 'fidget',
    'Respiración': 'respiracion',
    'Snake Neo': 'snake',
    '3 en Raya': 'tres_en_raya',
    'Ajedrez': 'ajedrez',
}

# Actualizar tipos
for nombre, tipo in mapeo_tipos.items():
    try:
        juego = Game.objects.get(nombre=nombre)
        juego.tipo = tipo
        juego.save()
        print(f"✓ Actualizado: {nombre} -> {tipo}")
    except Game.DoesNotExist:
        print(f"✗ No encontrado: {nombre}")

print("\nVerificación final:")
for juego in Game.objects.all():
    print(f"  - {juego.nombre}: {juego.tipo}")
