import os
import sys
import django

# Set console encoding to UTF-8
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from notificaciones.models import Notificacion
from django.contrib.auth.models import User

print(f"Total users: {User.objects.count()}")
for u in User.objects.all():
    print(f"User ID: {u.id} | Username: {u.username} | Email: {u.email} | Staff: {u.is_staff} | Superuser: {u.is_superuser}")

print(f"\nTotal notifications: {Notificacion.objects.count()}")
for n in Notificacion.objects.all().order_by('-fecha_creacion'):
    print(f"ID: {n.id} | User: {n.usuario.username} | Title: {n.titulo} | Date: {n.fecha_creacion} | Read: {n.leida}")
