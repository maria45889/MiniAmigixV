# ============================================================================
# LIST SONGS SCRIPT
# ============================================================================

import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.app.models import Cancion

songs = Cancion.objects.all().order_by('-id')[:10]
print(f"Total songs: {Cancion.objects.count()}")
for s in songs:
    print(f"ID: {s.id} | Nombre: {s.nombre} | Artista: {s.artista} | URL: {s.youtube_url} | YtID: {s.youtube_id}")
