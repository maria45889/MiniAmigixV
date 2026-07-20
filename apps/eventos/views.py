from django.shortcuts import render, redirect, get_object_or_404
from .models import Evento, CategoriaEvento
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from notificaciones.models import Notificacion
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models import Q
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def lista_eventos(request):
    # Obtener parámetros de filtro y búsqueda
    categoria_filtro = request.GET.get('categoria', '')
    busqueda = request.GET.get('q', '')
    vista = request.GET.get('vista', 'mes')  # mes, semana, lista
    
    # Filtrar eventos por usuario si está autenticado
    usuario = request.user if request.user.is_authenticated else None
    eventos = Evento.objects.filter(usuario=usuario).order_by('fecha') if usuario else Evento.objects.all().order_by('fecha')
    
    # Aplicar filtros
    if categoria_filtro:
        eventos = eventos.filter(categoria=categoria_filtro)
    
    if busqueda:
        eventos = eventos.filter(
            Q(titulo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(ubicacion__icontains=busqueda)
        )
    
    # Calcular estadísticas
    hoy = timezone.now().date()
    semana_inicio = hoy - timedelta(days=hoy.weekday())
    semana_fin = semana_inicio + timedelta(days=6)
    mes_inicio = hoy.replace(day=1)
    mes_fin = (mes_inicio + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    eventos_hoy = eventos.filter(fecha__date=hoy)
    eventos_semana = eventos.filter(fecha__date__range=[semana_inicio, semana_fin])
    eventos_mes = eventos.filter(fecha__date__range=[mes_inicio, mes_fin])
    
    # Próximo evento
    proximo_evento = eventos.filter(fecha__gte=timezone.now()).first()
    
    # Eventos futuros para la lista de próximos
    proximos_eventos = eventos.filter(fecha__gte=timezone.now())[:5]
    
    # Eventos de hoy y mañana para mini agenda
    eventos_hoy_lista = eventos.filter(fecha__date=hoy)
    manana = hoy + timedelta(days=1)
    eventos_manana = eventos.filter(fecha__date=manana)
    
    # Pre-process categories to extract emoji for display
    categorias_display = []
    for value, label in CategoriaEvento.choices:
        # Extract emoji (first character) for display
        emoji = label.split(' ')[0] if ' ' in label else label
        categorias_display.append({'value': value, 'label': label, 'emoji': emoji})
    
    context = {
        'eventos': eventos,
        'eventos_hoy': eventos_hoy,
        'eventos_semana': eventos_semana,
        'eventos_mes': eventos_mes,
        'proximo_evento': proximo_evento,
        'proximos_eventos': proximos_eventos,
        'eventos_hoy_lista': eventos_hoy_lista,
        'eventos_manana': eventos_manana,
        'categoria_filtro': categoria_filtro,
        'busqueda': busqueda,
        'vista': vista,
        'categorias': categorias_display,
    }
    
    return render(request, 'eventos/lista_eventos.html', context)

def crear_evento(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fecha = request.POST.get('fecha')
        categoria = request.POST.get('categoria', 'personal')
        ubicacion = request.POST.get('ubicacion', '')
        recordatorio_activo = request.POST.get('recordatorio_activo') == 'on'
        recordatorio_minutos_antes = int(request.POST.get('recordatorio_minutos_antes', 30))

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
                fecha=fecha_evento,
                categoria=categoria,
                ubicacion=ubicacion,
                recordatorio_activo=recordatorio_activo,
                recordatorio_minutos_antes=recordatorio_minutos_antes,
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

def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fecha = request.POST.get('fecha')
        categoria = request.POST.get('categoria', 'personal')
        ubicacion = request.POST.get('ubicacion', '')
        recordatorio_activo = request.POST.get('recordatorio_activo') == 'on'
        recordatorio_minutos_antes = int(request.POST.get('recordatorio_minutos_antes', 30))

        if titulo and fecha:
            from datetime import datetime
            fecha_evento = timezone.make_aware(datetime.fromisoformat(fecha))

            # Validar que la fecha sea presente o futura
            if fecha_evento < timezone.now():
                from django.contrib import messages
                messages.error(request, 'No puedes crear eventos en fechas pasadas.')
                return render(request, 'eventos/editar_evento.html', {'evento': evento})

            # Actualizar evento
            evento.titulo = titulo
            evento.descripcion = descripcion
            evento.fecha = fecha_evento
            evento.categoria = categoria
            evento.ubicacion = ubicacion
            evento.recordatorio_activo = recordatorio_activo
            evento.recordatorio_minutos_antes = recordatorio_minutos_antes
            evento.save()

            from django.contrib import messages
            messages.success(request, 'Evento actualizado exitosamente.')
            return redirect('lista_eventos')

    return render(request, 'eventos/editar_evento.html', {'evento': evento})
