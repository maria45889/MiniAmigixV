from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from apps.mongodb.models import MetricasSistemaMongo, EstadisticasUsuarioMongo
from notificaciones.models import Notificacion
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Verifica métricas y envía alertas cuando se detectan anomalías'

    def handle(self, *args, **options):
        self.stdout.write('=== Verificando alertas basadas en métricas ===')
        
        # Obtener métricas del sistema de hoy
        hoy = datetime.now().date()
        fecha_hoy = datetime.combine(hoy, datetime.min.time())
        metricas_hoy = MetricasSistemaMongo.objects(fecha=fecha_hoy).first()
        
        if not metricas_hoy:
            self.stdout.write('No hay métricas de hoy para verificar')
            return
        
        alertas_enviadas = 0
        
        # Alerta 1: Baja actividad de usuarios
        if metricas_hoy.usuarios_activos < 5:
            self.stdout.write('⚠ Alerta: Baja actividad de usuarios')
            self.enviar_alerta_admin(
                titulo='⚠ Alerta: Baja actividad de usuarios',
                mensaje=f'Solo {metricas_hoy.usuarios_activos} usuarios activos hoy. Normalmente debería haber más.',
                tipo='alerta'
            )
            alertas_enviadas += 1
        
        # Alerta 2: Picos de actividad inusual
        if metricas_hoy.total_chats > 100:
            self.stdout.write('⚠ Alerta: Pico de actividad inusual')
            self.enviar_alerta_admin(
                titulo='⚠ Alerta: Pico de actividad inusual',
                mensaje=f'{metricas_hoy.total_chats} chats hoy. Actividad significativamente alta.',
                tipo='info'
            )
            alertas_enviadas += 1
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Verificación completada. {alertas_enviadas} alertas enviadas'))
    
    def enviar_alerta_admin(self, titulo, mensaje, tipo):
        """Envía alerta a los administradores"""
        try:
            # Enviar notificación en el sistema
            for admin_email in getattr(settings, 'ADMIN_EMAILS', ['miniamigixv@gmail.com']):
                # Buscar usuario admin
                admin_user = User.objects.filter(email=admin_email).first()
                if admin_user:
                    Notificacion.objects.create(
                        usuario=admin_user,
                        titulo=titulo,
                        mensaje=mensaje,
                        tipo=tipo,
                        enlace='/mongodb/dashboard-analitica/'
                    )
            
            # Enviar email
            send_mail(
                titulo,
                f'{mensaje}\n\nFecha: {datetime.now().strftime("%d/%m/%Y %H:%M")}\n\nSaludos,\nMiniAmigixV',
                settings.DEFAULT_FROM_EMAIL,
                getattr(settings, 'ADMIN_EMAILS', ['miniamigixv@gmail.com']),
                fail_silently=True,
            )
        except Exception as e:
            self.stdout.write(f'✗ Error enviando alerta: {str(e)}')
