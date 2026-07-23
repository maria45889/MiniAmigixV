# Generated migration to fix NULL tema values

from django.db import migrations


def fix_tema_null(apps, schema_editor):
    """Set default 'dark' theme for profiles with NULL tema."""
    Perfil = apps.get_model('perfil', 'Perfil')
    Perfil.objects.filter(tema__isnull=True).update(tema='dark')


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0010_perfil_patito_accesorio_perfil_patito_color_cuerpo_and_more'),
    ]

    operations = [
        migrations.RunPython(fix_tema_null, migrations.RunPython.noop),
    ]
