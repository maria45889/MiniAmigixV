from django.shortcuts import render, redirect, get_object_or_404
from .models import Evento
from django.utils import timezone

def lista_eventos(request):
    eventos = Evento.objects.all().order_by('fecha')
    return render(request, 'eventos/lista_eventos.html', {'eventos': eventos})

def crear_evento(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fecha = request.POST.get('fecha')
        
        if titulo and fecha:
            Evento.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                fecha=fecha
            )
            return redirect('lista_eventos')
    
    return render(request, 'eventos/crear_evento.html')

def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        evento.delete()
        return redirect('lista_eventos')
    return redirect('lista_eventos')
