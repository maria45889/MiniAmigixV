import os
import sys
import django

if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.sugerencias.models import Sugerencia

print(f"Total suggestions: {Sugerencia.objects.count()}")
for s in Sugerencia.objects.all().order_by('-fecha_creacion'):
    print(f"ID: {s.id} | User: {s.usuario.username if s.usuario else 'Anon'} | Titulo: {s.titulo} | Estado: {s.estado} | Respondida: {bool(s.respuesta_admin)}")
