# Generated migration to fix naive datetimes

from django.db import migrations
from django.utils import timezone
import datetime


def fix_naive_datetimes(apps, schema_editor):
    """Convert naive datetimes to aware datetimes for existing events."""
    Evento = apps.get_model('eventos', 'Evento')
    
    for evento in Evento.objects.all():
        if evento.fecha and timezone.is_naive(evento.fecha):
            # Convert naive datetime to aware datetime using default timezone
            evento.fecha = timezone.make_aware(evento.fecha)
            evento.save(update_fields=['fecha'])


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0004_evento_categoria_evento_recordatorio_activo_and_more'),
    ]

    operations = [
        migrations.RunPython(fix_naive_datetimes, migrations.RunPython.noop),
    ]
