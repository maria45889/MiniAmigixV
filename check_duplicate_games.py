import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.app.models import Game

# Verificar juegos duplicados
juegos = Game.objects.all()
print(f"Total de juegos en base de datos: {juegos.count()}")
print("\nLista de juegos:")
for juego in juegos:
    print(f"  - ID: {juego.id}, Nombre: {juego.nombre}, Tipo: {juego.tipo}, Activo: {juego.activo}")

# Buscar duplicados por nombre
from django.db.models import Count
duplicados = Game.objects.values('nombre').annotate(count=Count('id')).filter(count__gt=1)
print(f"\nJuegos duplicados encontrados: {duplicados.count()}")
for dup in duplicados:
    print(f"  - Nombre: '{dup['nombre']}', Cantidad: {dup['count']}")
