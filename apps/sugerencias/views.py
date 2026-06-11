from django.shortcuts import render, redirect
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
