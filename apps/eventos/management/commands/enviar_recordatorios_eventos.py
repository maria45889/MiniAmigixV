from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.eventos.models import Evento
from apps.notificaciones.models import Notificacion
from django.contrib.auth.models import User
from apps.perfil.models import Perfil
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Envía recordatorios automáticos para eventos próximos'

    def handle(self, *args, **options):
        ahora = timezone.now()
        un_dia_despues = ahora + timedelta(days=1)
        una_hora_despues = ahora + timedelta(hours=1)

        # Eventos que faltan 1 día (24 horas)
        eventos_1dia = Evento.objects.filter(
            fecha__gte=ahora,
            fecha__lte=un_dia_despues,
            notificacion_1dia_enviada=False
        )

        for evento in eventos_1dia:
            try:
                # Crear notificación para todos los usuarios
                for usuario in User.objects.filter(is_active=True):
                    Notificacion.objects.create(
                        usuario=usuario,
                        titulo='📅 Recordatorio: Evento mañana',
                        mensaje=f'El evento "{evento.titulo}" es mañana a las {evento.fecha.strftime("%H:%M")}. ¡No olvides prepararte!',
                        tipo='evento',
                        enlace='/eventos/'
                    )
                    
                    # Enviar email si el usuario tiene email
                    if usuario.email:
                        try:
                            send_mail(
                                f'📅 Recordatorio: {evento.titulo} es mañana',
                                f'Hola {usuario.username},\n\nEste es un recordatorio de que el evento "{evento.titulo}" es mañana a las {evento.fecha.strftime("%H:%M")}.\n\n¡No olvides prepararte!\n\nSaludos,\nMiniAmigixV',
                                settings.DEFAULT_FROM_EMAIL,
                                [usuario.email],
                                fail_silently=True,
                            )
                        except Exception as e:
                            logger.error(f'Error al enviar email a {usuario.email}: {str(e)}')
                
                evento.notificacion_1dia_enviada = True
                evento.save()
                self.stdout.write(f'✓ Notificación de 1 día enviada para: {evento.titulo}')
            except Exception as e:
                logger.error(f'Error al enviar notificación de 1 día para {evento.titulo}: {str(e)}')

        # Eventos que faltan 1 hora
        eventos_1hora = Evento.objects.filter(
            fecha__gte=ahora,
            fecha__lte=una_hora_despues,
            notificacion_1hora_enviada=False
        )

        for evento in eventos_1hora:
            try:
                # Crear notificación para todos los usuarios
                for usuario in User.objects.filter(is_active=True):
                    Notificacion.objects.create(
                        usuario=usuario,
                        titulo='⏰ Recordatorio: Evento en 1 hora',
                        mensaje=f'El evento "{evento.titulo}" comienza en 1 hora a las {evento.fecha.strftime("%H:%M")}. ¡Es hora de prepararte!',
                        tipo='evento',
                        enlace='/eventos/'
                    )
                    
                    # Enviar email si el usuario tiene email
                    if usuario.email:
                        try:
                            send_mail(
                                f'⏰ Recordatorio: {evento.titulo} en 1 hora',
                                f'Hola {usuario.username},\n\nEste es un recordatorio de que el evento "{evento.titulo}" comienza en 1 hora a las {evento.fecha.strftime("%H:%M")}.\n\n¡Es hora de prepararte!\n\nSaludos,\nMiniAmigixV',
                                settings.DEFAULT_FROM_EMAIL,
                                [usuario.email],
                                fail_silently=True,
                            )
                        except Exception as e:
                            logger.error(f'Error al enviar email a {usuario.email}: {str(e)}')
                
                evento.notificacion_1hora_enviada = True
                evento.save()
                self.stdout.write(f'✓ Notificación de 1 hora enviada para: {evento.titulo}')
            except Exception as e:
                logger.error(f'Error al enviar notificación de 1 hora para {evento.titulo}: {str(e)}')

        self.stdout.write(self.style.SUCCESS('✓ Verificación de recordatorios completada'))
