from django.shortcuts import render, redirect
from perfil.models import Perfil
from django.http import JsonResponse
import json

def configuracion_view(request):
    if request.user.is_authenticated:
        perfil, created = Perfil.objects.get_or_create(usuario=request.user)

        if request.method == 'POST':
            perfil.tema = request.POST.get('tema', perfil.tema)
            perfil.idioma = request.POST.get('idioma', perfil.idioma)
            perfil.notificaciones_email = request.POST.get('notificaciones_email') == 'on'
            perfil.perfil_publico = request.POST.get('perfil_publico') == 'on'
            perfil.save()

            tema_actualizado = True
            return render(request, 'configuracion/configuracion.html', {
                'perfil': perfil,
                'tema_actualizado': tema_actualizado
            })

        return render(request, 'configuracion/configuracion.html', {'perfil': perfil})
    else:
        return render(request, 'configuracion/configuracion.html', {'perfil': None})
