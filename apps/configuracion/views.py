from django.shortcuts import render, redirect
from perfil.models import Perfil
from django.http import JsonResponse
import json
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm


@login_required
def cambiar_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantiene la sesión activa tras el cambio
            messages.success(request, 'Tu contraseña ha sido actualizada con éxito.')
            return redirect('configuracion_view')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'cambiar_password.html', {'form': form})

@login_required
def configuracion_view(request):
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        perfil.tema = request.POST.get('tema', perfil.tema)
        perfil.idioma = request.POST.get('idioma', perfil.idioma)
        perfil.notificaciones_email = request.POST.get('notificaciones_email') == 'on'
        perfil.notificaciones_push = request.POST.get('notificaciones_push') == 'on'
        perfil.perfil_publico = request.POST.get('perfil_publico') == 'on'
        perfil.tamano_fuente = request.POST.get('tamano_fuente', perfil.tamano_fuente)
        perfil.animaciones = request.POST.get('animaciones') == 'on'
        perfil.sonidos = request.POST.get('sonidos') == 'on'
        perfil.actividad_en_linea = request.POST.get('actividad_en_linea') == 'on'
        # Reloj inteligente
        perfil.formato_reloj = request.POST.get('formato_reloj', perfil.formato_reloj)
        perfil.mostrar_segundos = request.POST.get('mostrar_segundos') == 'on'
        perfil.mostrar_fecha = request.POST.get('mostrar_fecha') == 'on'
        perfil.zona_horaria = request.POST.get('zona_horaria', perfil.zona_horaria)
        perfil.save()
        
        messages.success(request, 'Configuración actualizada correctamente.')
        return redirect('configuracion_view')
        
    return render(request, 'configuracion.html', {'perfil': perfil})