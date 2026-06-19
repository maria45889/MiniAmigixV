from django.shortcuts import render, redirect, get_object_or_404
from .models import Evento
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from notificaciones.models import Notificacion
import logging

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

            # Crear notificación para el usuario
            if request.user.is_authenticated:
                try:
                    Notificacion.objects.create(
                        usuario=request.user,
                        titulo='📅 Evento creado',
                        mensaje=f'Tu evento "{titulo}" ha sido creado para el {fecha_evento.strftime("%d/%m/%Y %H:%M")}.',
                        tipo='evento',
                        enlace='/eventos/'
                    )
                except Exception as e:
                    logging.error(f"Error al crear notificación de evento: {str(e)}")

            return redirect('lista_eventos')

    return render(request, 'eventos/crear_evento.html')

def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        evento.delete()
        return redirect('lista_eventos')
    return redirect('lista_eventos')
