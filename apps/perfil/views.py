from django.shortcuts import render, redirect
from .models import Perfil
from django.contrib.auth.models import User
from django.utils import timezone
from notificaciones.models import Notificacion
from eventos.models import Evento

def ver_perfil(request):
    if request.user.is_authenticated:
        perfil, created = Perfil.objects.get_or_create(usuario=request.user)
        try:
            total_notificaciones = Notificacion.objects.filter(usuario=request.user).count()
            total_eventos = Evento.objects.filter(usuario=request.user).count()
        except Exception:
            total_notificaciones = 0
            total_eventos = 0
            
        if perfil.creado:
            dias_activo = (timezone.now().date() - perfil.creado.date()).days
        else:
            dias_activo = 0
        return render(request, 'perfil/index.html', {
            'perfil': perfil,
            'total_notificaciones': total_notificaciones,
            'total_eventos': total_eventos,
            'dias_activo': dias_activo
        })
    else:
        return render(request, 'perfil/index.html', {'perfil': None})

def editar_perfil(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        # Actualizar campos
        perfil.bio = request.POST.get('bio', perfil.bio or '')
        perfil.tema = request.POST.get('tema', perfil.tema or 'dark')
        perfil.idioma = request.POST.get('idioma', perfil.idioma or 'es')
        
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        if fecha_nacimiento:
            perfil.fecha_nacimiento = fecha_nacimiento
        
        if 'avatar' in request.FILES and request.FILES['avatar']:
            perfil.avatar = request.FILES['avatar']
        
        perfil.save()
        return redirect('perfil')
    
    return render(request, 'perfil/editar.html', {'perfil': perfil})
