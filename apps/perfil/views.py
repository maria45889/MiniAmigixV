from django.shortcuts import render, redirect
from .models import Perfil
from django.contrib.auth.models import User

def ver_perfil(request):
    if request.user.is_authenticated:
        perfil, created = Perfil.objects.get_or_create(usuario=request.user)
        return render(request, 'perfil/index.html', {'perfil': perfil})
    else:
        return render(request, 'perfil/index.html', {'perfil': None})

def editar_perfil(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        perfil.bio = request.POST.get('bio', '')
        perfil.tema = request.POST.get('tema', 'dark')
        perfil.idioma = request.POST.get('idioma', 'es')
        
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        if fecha_nacimiento:
            perfil.fecha_nacimiento = fecha_nacimiento
        
        if 'avatar' in request.FILES:
            perfil.avatar = request.FILES['avatar']
        
        perfil.save()
        return redirect('ver_perfil')
    
    return render(request, 'perfil/editar.html', {'perfil': perfil})
