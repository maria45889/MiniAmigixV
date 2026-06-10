from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import TicketSoporte

def lista_tickets(request):
    tickets = TicketSoporte.objects.all().order_by('-fecha_creacion')
    return render(request, 'soporte/lista_tickets.html', {'tickets': tickets})

def crear_ticket(request):
    if request.method == 'POST':
        asunto = request.POST.get('asunto')
        descripcion = request.POST.get('descripcion')
        prioridad = request.POST.get('prioridad', 'media')
        
        if asunto and descripcion:
            TicketSoporte.objects.create(
                asunto=asunto,
                descripcion=descripcion,
                prioridad=prioridad,
                usuario=request.user if request.user.is_authenticated else None
            )
            return redirect('lista_tickets')
    
    return render(request, 'soporte/crear_ticket.html')

def soporte_home(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        mensaje = request.POST.get("mensaje")

        asunto = f"🛟 Soporte de {nombre}"

        contenido = f"""
        NUEVO MENSAJE DE SOPORTE

        Nombre: {nombre}
        Email: {email}

        Mensaje:
        {mensaje}
        """

        try:
            send_mail(
                asunto,
                contenido,
                settings.EMAIL_HOST_USER,
                ["miniamigixv@gmail.com"]
            )
            return render(request, "soporte/index.html", {"enviado": True})
        except Exception as e:
            return render(request, "soporte/index.html", {"error": True})

    return render(request, "soporte/index.html")
