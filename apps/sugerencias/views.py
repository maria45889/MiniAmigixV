from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Sugerencia

def lista_sugerencias(request):
    sugerencias = Sugerencia.objects.all().order_by('-fecha_creacion')
    return render(request, 'sugerencias/lista_sugerencias.html', {'sugerencias': sugerencias})

def crear_sugerencia(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        categoria = request.POST.get('categoria', 'mejora')
        
        if titulo and descripcion:
            Sugerencia.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                categoria=categoria,
                usuario=request.user if request.user.is_authenticated else None
            )
            return redirect('lista_sugerencias')
    
    return render(request, 'sugerencias/crear_sugerencia.html')

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_sugerencias(request):
    sugerencias = Sugerencia.objects.all().order_by('-fecha_creacion')
    return render(request, 'sugerencias/admin_sugerencias.html', {'sugerencias': sugerencias})

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
                    send_mail(
                        f'🎉 Respuesta a tu sugerencia: {sugerencia.titulo}',
                        f'Hola {sugerencia.usuario.username},\n\nTu sugerencia ha recibido una respuesta:\n\n{respuesta}\n\nSaludos,\nEl equipo de MiniAmigixV',
                        settings.EMAIL_HOST_USER,
                        [sugerencia.usuario.email],
                    )
                except:
                    pass
            
            return redirect('admin_sugerencias')
    
    return render(request, 'sugerencias/responder_sugerencia.html', {'sugerencia': sugerencia})
