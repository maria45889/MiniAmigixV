from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Sugerencia
from notificaciones.models import Notificacion
import logging

@login_required
def lista_sugerencias(request):
    # Verificar si es administrador (email miniamigixv@gmail.com o is_staff)
    es_admin = request.user.is_staff or request.user.email == 'miniamigixv@gmail.com'
    
    if es_admin:
        # Administrador ve todas las sugerencias
        sugerencias = Sugerencia.objects.all().order_by('-fecha_creacion')
    else:
        # Usuario normal solo ve sus propias sugerencias
        sugerencias = Sugerencia.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    # Calcular estadísticas para el frontend
    total_sugerencias = sugerencias.count()
    pendientes = sugerencias.filter(estado='pendiente').count()
    aprobadas = sugerencias.filter(estado='aprobada').count()
    
    return render(request, 'sugerencias/lista_sugerencias.html', {
        'sugerencias': sugerencias,
        'total_sugerencias': total_sugerencias,
        'pendientes': pendientes,
        'aprobadas': aprobadas,
        'es_admin': es_admin
    })

def crear_sugerencia(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        categoria = request.POST.get('categoria', 'mejora')
        
        if titulo and descripcion:
            sugerencia = Sugerencia.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                categoria=categoria,
                usuario=request.user if request.user.is_authenticated else None
            )
            
            # Enviar email al administrador
            try:
                contenido_html = render_to_string('emails/sugerencia.html', {
                    'nombre': request.user.username if request.user.is_authenticated else 'Usuario anónimo',
                    'email': request.user.email if request.user.is_authenticated else 'No proporcionado',
                    'mensaje': descripcion,
                    'categoria': categoria,
                    'fecha': timezone.now().strftime('%d/%m/%Y %H:%M'),
                })
                
                contenido_texto = f"""
Nueva Sugerencia de MiniAmigixV

De: {request.user.username if request.user.is_authenticated else 'Usuario anónimo'}
Email: {request.user.email if request.user.is_authenticated else 'No proporcionado'}
Categoría: {categoria}
Fecha: {timezone.now().strftime('%d/%m/%Y %H:%M')}

Mensaje:
{descripcion}
                """.strip()
                
                email = EmailMultiAlternatives(
                    f'🎨 Nueva sugerencia: {titulo}',
                    contenido_texto,
                    settings.EMAIL_HOST_USER,
                    settings.ADMIN_EMAILS,
                )
                email.attach_alternative(contenido_html, "text/html")
                email.encoding = 'utf-8'
                email.send()
            except Exception as e:
                print(f"Error enviando email de sugerencia: {e}")
                import traceback
                traceback.print_exc()

            # Crear notificación para el usuario
            if request.user.is_authenticated:
                try:
                    Notificacion.objects.create(
                        usuario=request.user,
                        titulo='💡 Sugerencia enviada',
                        mensaje=f'Tu sugerencia "{titulo}" ha sido enviada. Te notificaremos cuando haya una respuesta.',
                        tipo='success',
                        enlace='/sugerencias/'
                    )
                except Exception as e:
                    logging.error(f"Error al crear notificación de sugerencia: {str(e)}")

            return redirect('lista_sugerencias')
    
    return render(request, 'sugerencias/crear_sugerencia.html')

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_sugerencias(request):
    sugerencias = Sugerencia.objects.all().order_by('-fecha_creacion')
    
    # Calcular estadísticas
    total_sugerencias = sugerencias.count()
    sugerencias_pendientes = sugerencias.filter(estado='pendiente').count()
    sugerencias_en_revision = sugerencias.filter(estado='en_revision').count()
    sugerencias_aprobadas = sugerencias.filter(estado='aprobada').count()
    
    return render(request, 'admin_sugerencias.html', {
        'sugerencias': sugerencias,
        'total_sugerencias': total_sugerencias,
        'sugerencias_pendientes': sugerencias_pendientes,
        'sugerencias_en_revision': sugerencias_en_revision,
        'sugerencias_aprobadas': sugerencias_aprobadas
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def responder_sugerencia(request, sugerencia_id):
    sugerencia = get_object_or_404(Sugerencia, id=sugerencia_id)
    
    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')
        nuevo_estado = request.POST.get('estado')
        
        if respuesta:
            sugerencia.respuesta_admin = respuesta
            sugerencia.fecha_respuesta = timezone.now()
            sugerencia.respondido_por = request.user
            
            if nuevo_estado:
                sugerencia.estado = nuevo_estado
            
            sugerencia.save()
            
            # Enviar email de notificación al usuario si tiene email
            if sugerencia.usuario and sugerencia.usuario.email:
                try:
                    email = EmailMultiAlternatives(
                        f'🎉 Respuesta a tu sugerencia: {sugerencia.titulo}',
                        f'Hola {sugerencia.usuario.username},\n\nTu sugerencia ha recibido una respuesta:\n\n{respuesta}\n\nSaludos,\nEl equipo de MiniAmigixV',
                        settings.DEFAULT_FROM_EMAIL,
                        [sugerencia.usuario.email],
                    )
                    email.encoding = 'utf-8'
                    import threading
                    threading.Thread(target=email.send).start()
                except:
                    pass
            
            # Crear notificación en el sistema
            if sugerencia.usuario:
                try:
                    Notificacion.objects.create(
                        usuario=sugerencia.usuario,
                        titulo=f'🎉 Respuesta a tu sugerencia: {sugerencia.titulo}',
                        mensaje=f'Tu sugerencia ha recibido una respuesta: {respuesta}',
                        tipo='success',
                        leida=False,
                        enlace='/sugerencias/'
                    )
                except:
                    pass
            
            return redirect('admin_sugerencias')
    
    return render(request, 'sugerencias/responder_sugerencia.html', {'sugerencia': sugerencia})
