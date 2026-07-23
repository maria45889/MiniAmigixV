import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.app.models import Game

juego = Game.objects.filter(nombre='3 en Raya').first()
if juego:
    juego.icono = 'X'
    juego.save()
    print('Icono actualizado a X')
else:
    print('Juego no encontrado')
