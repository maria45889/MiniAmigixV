import os
import sys
import django

if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.soporte.models import TicketSoporte

print(f"Total tickets: {TicketSoporte.objects.count()}")
for t in TicketSoporte.objects.all().order_by('-fecha_creacion'):
    print(f"ID: {t.id} | User: {t.usuario.username} | Asunto: {t.asunto} | Respondido: {t.respondido} | Respondido Por: {t.respondido_por.username if t.respondido_por else 'None'}")
