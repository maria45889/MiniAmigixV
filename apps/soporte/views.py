from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from .models import TicketSoporte
from notificaciones.models import Notificacion
import logging

def lista_tickets(request):
    tickets = TicketSoporte.objects.all().order_by('-fecha_creacion')
    return render(request, 'soporte/lista_tickets.html', {'tickets': tickets})

def crear_ticket(request):
    if request.method == 'POST':
        asunto = request.POST.get('asunto')
        descripcion = request.POST.get('descripcion')
        prioridad = request.POST.get('prioridad', 'media')

        if asunto and descripcion:
            ticket = TicketSoporte.objects.create(
                asunto=asunto,
                descripcion=descripcion,
                prioridad=prioridad,
                usuario=request.user if request.user.is_authenticated else None
            )

            # Crear notificación para el usuario
            if request.user.is_authenticated:
                try:
                    Notificacion.objects.create(
                        usuario=request.user,
                        titulo='🎫 Ticket de soporte creado',
                        mensaje=f'Tu ticket "{asunto}" ha sido creado. Te responderemos pronto.',
                        tipo='success',
                        enlace='/soporte/lista_tickets/'
                    )
                except Exception as e:
                    logging.error(f"Error al crear notificación de ticket: {str(e)}")

            return redirect('lista_tickets')

    return render(request, 'soporte/crear_ticket.html')

def soporte_home(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        mensaje = request.POST.get("mensaje")
        categoria = request.POST.get("asunto", "general")

        categorias_map = {
            "general": "Consulta general",
            "bug": "Reportar un error",
            "cuenta": "Problema con cuenta",
            "sugerencia": "Sugerencia",
            "otro": "Otro",
        }
        categoria_texto = categorias_map.get(categoria, categoria)

        # Estilos de badge según categoría
        badge_styles = {
            "general":    {"bg": "rgba(6,182,212,0.15)",  "border": "rgba(6,182,212,0.3)",  "color": "#06b6d4", "emoji": "📋"},
            "bug":        {"bg": "rgba(239,68,68,0.15)",  "border": "rgba(239,68,68,0.3)",  "color": "#ef4444", "emoji": "🐛"},
            "cuenta":     {"bg": "rgba(245,158,11,0.15)", "border": "rgba(245,158,11,0.3)", "color": "#f59e0b", "emoji": "🔑"},
            "sugerencia": {"bg": "rgba(16,185,129,0.15)", "border": "rgba(16,185,129,0.3)", "color": "#10b981", "emoji": "💡"},
            "otro":       {"bg": "rgba(167,139,250,0.15)","border": "rgba(167,139,250,0.3)","color": "#a78bfa", "emoji": "📌"},
        }
        badge = badge_styles.get(categoria, badge_styles["general"])

        asunto_email = f"🛟 [{categoria_texto}] Soporte de {nombre}"

        # Texto plano (fallback)
        contenido_texto = f"""
        NUEVO MENSAJE DE SOPORTE

        Nombre: {nombre}
        Email: {email}
        Categoría: {categoria_texto}

        Mensaje:
        {mensaje}
        """

        # Renderizar plantilla HTML
        fecha_actual = timezone.now().strftime("%d/%m/%Y a las %H:%M")
        contenido_html = render_to_string("email_soporte.html", {
            "nombre": nombre,
            "email": email,
            "mensaje": mensaje,
            "categoria": categoria_texto,
            "categoria_emoji": badge["emoji"],
            "badge_bg": badge["bg"],
            "badge_border": badge["border"],
            "badge_color": badge["color"],
            "fecha": fecha_actual,
        })

        try:
            email = EmailMultiAlternatives(
                asunto_email,
                contenido_texto,
                settings.EMAIL_HOST_USER,
                settings.ADMIN_EMAILS,
            )
            email.attach_alternative(contenido_html, "text/html")
            email.encoding = 'utf-8'
            resultado = email.send()
            
            # Verificar si el correo se envió correctamente
            if resultado == 0:
                print(f"ERROR: El correo no se envió. Configuración SMTP: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
                return render(request, "soporte/index.html", {"error": True, "error_msg": "No se pudo enviar el correo. Verifica la configuración SMTP."})

            # Crear notificación si el usuario está autenticado
            if request.user.is_authenticated:
                try:
                    Notificacion.objects.create(
                        usuario=request.user,
                        titulo='📧 Mensaje de soporte enviado',
                        mensaje=f'Tu mensaje de soporte sobre "{categoria_texto}" ha sido enviado. Te responderemos pronto.',
                        tipo='success',
                        enlace='/soporte/'
                    )
                except Exception as e:
                    logging.error(f"Error al crear notificación de soporte: {str(e)}")

            return render(request, "soporte/index.html", {"enviado": True})
        except Exception as e:
            print(f"ERROR al enviar correo: {str(e)}")
            print(f"Configuración SMTP: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}, TLS: {settings.EMAIL_USE_TLS}")
            return render(request, "soporte/index.html", {"error": True, "error_msg": f"Error: {str(e)}"})

    return render(request, "soporte/index.html")

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_tickets(request):
    tickets = TicketSoporte.objects.all().order_by('-fecha_creacion')
    return render(request, 'soporte/admin_tickets.html', {'tickets': tickets})

@login_required
@user_passes_test(lambda u: u.is_staff)
def responder_ticket(request, ticket_id):
    ticket = get_object_or_404(TicketSoporte, id=ticket_id)
    
    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')
        nuevo_estado = request.POST.get('estado')
        
        if respuesta:
            ticket.respuesta_admin = respuesta
            ticket.fecha_respuesta = timezone.now()
            ticket.respondido_por = request.user
            
            if nuevo_estado:
                ticket.estado = nuevo_estado
                if nuevo_estado == 'resuelto':
                    ticket.fecha_resolucion = timezone.now()
            
            ticket.save()
            
            # Enviar email de notificación al usuario si tiene email
            if ticket.usuario and ticket.usuario.email:
                try:
                    email = EmailMultiAlternatives(
                        f'🎉 Respuesta a tu ticket: {ticket.asunto}',
                        f'Hola {ticket.usuario.username},\n\nTu ticket ha recibido una respuesta:\n\n{respuesta}\n\nSaludos,\nEl equipo de MiniAmigixV',
                        settings.DEFAULT_FROM_EMAIL,
                        [ticket.usuario.email],
                    )
                    email.encoding = 'utf-8'
                    email.send()
                except:
                    pass
            
            # Crear notificación en el sistema
            if ticket.usuario:
                try:
                    Notificacion.objects.create(
                        usuario=ticket.usuario,
                        titulo=f'🎉 Respuesta a tu ticket: {ticket.asunto}',
                        mensaje=f'Tu ticket ha recibido una respuesta: {respuesta}',
                        tipo='success',
                        leida=False
                    )
                except:
                    pass
            
            return redirect('admin_tickets')
    
    return render(request, 'soporte/responder_ticket.html', {'ticket': ticket})
