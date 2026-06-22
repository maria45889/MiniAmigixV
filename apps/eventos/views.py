from django.shortcuts import render, redirect, get_object_or_404
from .models import Evento
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from notificaciones.models import Notificacion
from django.core.mail import send_mail
from django.conf import settings
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
            fecha_evento = datetime.fromisoformat(fecha)

            # Validar que la fecha sea presente o futura
            if fecha_evento < timezone.now():
                from django.contrib import messages
                messages.error(request, 'No puedes crear eventos en fechas pasadas.')
                return render(request, 'eventos/crear_evento.html')

            evento = Evento.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                fecha=fecha
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

                    # Enviar email de confirmación
                    if request.user.email:
                        try:
                            send_mail(
                                f'📅 Evento creado: {titulo}',
                                f'Hola {request.user.username},\n\nTu evento "{titulo}" ha sido creado exitosamente.\n\nFecha: {fecha_evento.strftime("%d/%m/%Y %H:%M")}\nDescripción: {descripcion or "Sin descripción"}\n\nTe enviaremos recordatorios automáticos antes del evento.\n\nSaludos,\nMiniAmigixV',
                                settings.DEFAULT_FROM_EMAIL,
                                [request.user.email],
                                fail_silently=True,
                            )
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
