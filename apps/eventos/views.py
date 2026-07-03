from django.shortcuts import render, redirect, get_object_or_404
from .models import Evento
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from notificaciones.models import Notificacion
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

def lista_eventos(request):
    eventos = Evento.objects.all().order_by('fecha')
    return render(request, 'eventos/lista_eventos.html', {'eventos': eventos})

def crear_evento(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fecha = request.POST.get('fecha')

        if titulo and fecha:
            from datetime import datetime
            fecha_evento = timezone.make_aware(datetime.fromisoformat(fecha))

            # Validar que la fecha sea presente o futura
            if fecha_evento < timezone.now():
                from django.contrib import messages
                messages.error(request, 'No puedes crear eventos en fechas pasadas.')
                return render(request, 'eventos/crear_evento.html')

            # Evitar duplicados: mismo título + fecha + usuario
            usuario = request.user if request.user.is_authenticated else None
            if Evento.objects.filter(titulo=titulo, fecha=fecha, usuario=usuario).exists():
                from django.contrib import messages
                messages.warning(request, 'Ya existe un evento con ese título y fecha.')
                return redirect('lista_eventos')

            evento = Evento.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                fecha=fecha,
                usuario=usuario
            )

            # Crear notificación mejorada para el usuario
            if request.user.is_authenticated:
                try:
                    # Calcular días restantes
                    dias_restantes = (fecha_evento - timezone.now()).days
                    if dias_restantes == 0:
                        texto_tiempo = "hoy"
                    elif dias_restantes == 1:
                        texto_tiempo = "mañana"
                    else:
                        texto_tiempo = f"en {dias_restantes} días"

                    Notificacion.objects.create(
                        usuario=request.user,
                        titulo='📅 Evento creado exitosamente',
                        mensaje=f'Tu evento "{titulo}" está programado para {texto_tiempo} ({fecha_evento.strftime("%d/%m/%Y %H:%M")}). Te enviaremos recordatorios automáticos.',
                        tipo='evento',
                        enlace='/eventos/'
                    )

                    # Enviar email de confirmación con HTML
                    if request.user.email:
                        try:
                            subject = f'📅 Evento creado: {titulo}'
                            from_email = settings.DEFAULT_FROM_EMAIL
                            to_email = [request.user.email]
                            
                            # Renderizar HTML
                            html_content = render_to_string('emails/evento_creado.html', {
                                'username': request.user.username,
                                'titulo': titulo,
                                'fecha': fecha_evento.strftime("%d/%m/%Y %H:%M"),
                                'descripcion': descripcion or "Sin descripción",
                                'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000')
                            })
                            
                            # Crear email con HTML
                            email = EmailMultiAlternatives(subject, '', from_email, to_email)
                            email.attach_alternative(html_content, 'text/html')
                            email.send(fail_silently=False)
                        except Exception as e:
                            logger.error(f'Error al enviar email de confirmación: {str(e)}')

                except Exception as e:
                    logger.error(f"Error al crear notificación de evento: {str(e)}")

            return redirect('lista_eventos')

    return render(request, 'eventos/crear_evento.html')

def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        evento.delete()
        return redirect('lista_eventos')
    return redirect('lista_eventos')
