from django.shortcuts import render, redirect
from perfil.models import Perfil

def configuracion_view(request):
    if request.user.is_authenticated:
        perfil, created = Perfil.objects.get_or_create(usuario=request.user)
        
        if request.method == 'POST':
            perfil.tema = request.POST.get('tema', 'dark')
            perfil.idioma = request.POST.get('idioma', 'es')
            perfil.save()
            
            # Actualizar tema en localStorage
            return render(request, 'configuracion/configuracion.html', {
                'perfil': perfil,
                'tema_actualizado': True
            })
        
        return render(request, 'configuracion/configuracion.html', {'perfil': perfil})
    else:
        return render(request, 'configuracion/configuracion.html', {'perfil': None})
