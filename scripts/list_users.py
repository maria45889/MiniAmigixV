import os
import sys
import pathlib
import django

# Asegurar que el directorio raíz del proyecto está en sys.path
root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
qs = User.objects.order_by('-date_joined')[:20]
for u in qs:
    print(u.id, u.username, u.email or '<no-email>', u.date_joined.isoformat(), 'active' if u.is_active else 'inactive')
