from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import mail_admins, send_mail
from django.contrib.admin.views.decorators import staff_member_required
from .admin_utils import admin_owner_required

from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
import json
import os
from .models import Profile, SupportTicket, Sugerencia


def login_view(request):
    google_auth_enabled = bool(
        settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY and settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
    )

    next_url = request.GET.get('next') or request.POST.get('next') or ''

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if email:
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                user = None
        else:
            user = None

        if user is not None:
            login(request, user)
            # Create or get profile for user
            Profile.objects.get_or_create(user=user)

            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                return redirect(next_url)
            return redirect("home")
        else:
            messages.error(request, "Credenciales inválidas")

    return render(request, "users/login.html", {
        'google_auth_enabled': google_auth_enabled,
        'next': next_url,
    })


def register_view(request):
    google_auth_enabled = bool(
        settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY and settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
    )

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado")
            return render(request, "users/register.html", {
                'google_auth_enabled': google_auth_enabled,
            })

        # Create user with email as username (for simplicity)
        username = email.split('@')[0]  # Use part before @ as username
        # Ensure username is unique
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = name  # Store name in first_name field
        user.save()
        # Create profile for new user
        Profile.objects.create(user=user)
        
        messages.success(request, "Cuenta creada correctamente. Ahora puedes iniciar sesión.")
        return redirect("login")

    return render(request, "users/register.html", {
        'google_auth_enabled': google_auth_enabled,
    })


def home_view(request):
    return render(request, "home.html")


@login_required
def support_view(request):
    institutional_info = {
        'misión': 'Nuestra misión es ofrecer una plataforma inteligente y accesible que ayude a los usuarios a gestionar su vida digital con soporte integrado, personalización y recursos prácticos.',
        'visión': 'Ser el asistente digital de referencia en América Latina para usuarios que buscan productividad, entretenimiento y soporte técnico dentro de una sola aplicación.',
        'descripción': 'MiniAmigixV combina herramientas de productividad, comunicación y entretenimiento para que los usuarios encuentren ayuda rápida, diversión y soluciones en un mismo lugar.',
        'objetivos': [
            'Proporcionar respuestas inmediatas y contextualizadas a las necesidades de los usuarios.',
            'Permitir la gestión de eventos, estudios, clima y traducciones con una experiencia amigable.',
            'Ofrecer un canal de soporte claro, directo y eficiente para resolver dudas y problemas.',
        ],
        'apoyo': 'Brindamos orientación, soporte técnico y una experiencia personalizada para que cada usuario pueda sacar el máximo provecho de la plataforma.',
    }

    support_tickets = SupportTicket.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        tipo = request.POST.get('tipo', 'consulta')
        prioridad = request.POST.get('prioridad', 'media')

        if not title or not description:
            messages.error(request, 'Por favor ingresa un título y una descripción para tu consulta de soporte.')
            return redirect('soporte')

        ticket = SupportTicket.objects.create(
            user=request.user,
            title=title,
            description=description,
            tipo=tipo,
            prioridad=prioridad,
        )

        subject = f"[Soporte MiniAmigixV] Nuevo ticket: {ticket.title}"
        message = (
            f"Usuario: {request.user.get_full_name() or request.user.username} <{request.user.email}>\n"
            f"Tipo: {ticket.get_tipo_display()}\n"
            f"Prioridad: {ticket.get_prioridad_display()}\n"
            f"Creado en: {ticket.created_at.strftime('%d/%m/%Y %H:%M')}\n\n"
            f"Descripción:\n{ticket.description}\n"
        )

        try:
            # 1) Notificar al admin
            mail_admins(subject, message, fail_silently=False)

            # 2) Acuse/confirmación al usuario por correo
            # (opción B solicitada)
            user_subject = f"[MiniAmigixV] Confirmación de tu ticket: {ticket.title}"
            user_message = (
                f"Hola {request.user.get_full_name() or request.user.username},\n\n"
                "Recibimos tu solicitud de soporte y el equipo de MiniAmigixV ya fue notificado.\n\n"
                f"Título: {ticket.title}\n"
                f"Tipo: {ticket.get_tipo_display()}\n"
                f"Prioridad: {ticket.get_prioridad_display()}\n"
                f"Creado en: {ticket.created_at.strftime('%d/%m/%Y %H:%M')}\n\n"
                "Cuando el administrador responda, también recibirás un correo con la respuesta.\n\n"
                "Gracias por usar MiniAmigixV."
            )

            if request.user.email:
                send_mail(
                    user_subject,
                    user_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                    fail_silently=False,
                )

            messages.success(
                request,
                'Tu consulta de soporte fue enviada. El equipo de administración recibió una notificación por correo y también te enviamos una confirmación por correo.'
            )
        except Exception as error:
            messages.error(request, f'No se pudo enviar el correo de notificación/acuse: {error}')


        return redirect('soporte')

    return render(request, 'soporte/index.html', {
        'institutional_info': institutional_info,
        'soportes': support_tickets,
    })


@login_required
@admin_owner_required
def admin_support_view(request):

    tickets = SupportTicket.objects.select_related('user', 'respondido_por').order_by('-created_at')

    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        respuesta = request.POST.get('respuesta', '').strip()
        estado = request.POST.get('estado', 'resuelto')

        if not ticket_id or not respuesta:
            messages.error(request, 'Debes agregar una respuesta antes de enviar.')
            return redirect('admin_soporte')

        try:
            ticket = SupportTicket.objects.get(id=ticket_id)
        except SupportTicket.DoesNotExist:
            messages.error(request, 'Ticket de soporte no encontrado.')
            return redirect('admin_soporte')

        ticket.respuesta = respuesta
        ticket.respondido_por = request.user
        ticket.respondido_en = timezone.now()
        ticket.estado = estado
        ticket.save()

        if ticket.user.email:
            subject = f"Respuesta a tu ticket de soporte: {ticket.title}"
            message = (
                f"Hola {ticket.user.get_full_name() or ticket.user.username},\n\n"
                f"Tu solicitud de soporte ha recibido una respuesta del administrador.\n\n"
                f"Título: {ticket.title}\n"
                f"Tipo: {ticket.get_tipo_display()}\n"
                f"Prioridad: {ticket.get_prioridad_display()}\n"
                f"Estado: {ticket.get_estado_display()}\n\n"
                f"Respuesta:\n{ticket.respuesta}\n\n"
                "Gracias por usar MiniAmigixV."
            )
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [ticket.user.email],
                    fail_silently=True,
                )
            except Exception:
                pass

        messages.success(request, f'Respuesta enviada al ticket #{ticket.id}.')
        return redirect('admin_soporte')

    return render(request, 'soporte/admin_panel.html', {
        'tickets': tickets,
    })


def google_auth_view(request):
    if settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY and settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET:
        return redirect(reverse('social:begin', args=['google-oauth2']))

    messages.error(
        request,
        'El inicio de sesión con Google requiere configurar OAuth en el servidor.'
    )
    return redirect('login')


@login_required
def profile_view(request):
    """User profile page"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'users/profile.html', {
        'user': request.user,
        'profile': profile
    })


@login_required
@require_POST
def crear_sugerencia(request):
    titulo = (request.POST.get('titulo') or '').strip()
    descripcion = (request.POST.get('descripcion') or '').strip()
    tipo = (request.POST.get('tipo') or 'idea').strip()

    if not titulo or not descripcion:
        return JsonResponse({'success': False, 'error': 'Título y descripción son requeridos.'}, status=400)

    if tipo not in dict(Sugerencia.TIPO_CHOICES):
        # fallback seguro
        tipo = 'idea'

    sugerencia = Sugerencia.objects.create(
        user=request.user,
        titulo=titulo,
        descripcion=descripcion,
        tipo=tipo,
        estado='pendiente',
    )

    # Email siempre al admin destino (servidor -> tu correo)
    destino = ['miniamigixv@gmail.com']
    remitente = settings.DEFAULT_FROM_EMAIL

    now = timezone.localtime(timezone.now())
    autor_nombre = request.user.get_full_name() or request.user.username
    autor_email = request.user.email or '(sin email)'

    subject = f"[MiniAmigixV] Nueva sugerencia: {sugerencia.titulo}"
    message = (
        "Se ha enviado una nueva sugerencia desde la web de MiniAmigixV.\n\n"
        f"Autor: {autor_nombre}\n"
        f"Email autor: {autor_email}\n"
        f"Fecha/hora: {now.strftime('%d/%m/%Y %H:%M')}\n\n"
        f"Tipo: {sugerencia.get_tipo_display()}\n"
        f"Estado: {sugerencia.get_estado_display()}\n\n"
        "Descripción:\n"
        f"{sugerencia.descripcion}\n"
    )

    try:
        send_mail(
            subject,
            message,
            remitente,
            destino,
            fail_silently=False,
        )
    except Exception:
        # Guardamos igual la sugerencia; fallar el email no debe romper el flujo
        pass

    return JsonResponse({'success': True})


@login_required
@require_POST
@csrf_exempt
def update_profile(request):
    """Update profile information"""
    try:
        if request.content_type and request.content_type.startswith('multipart/form-data'):
            data = request.POST.dict()
        else:
            body_text = request.body.decode('utf-8') if hasattr(request.body, 'decode') else request.body
            data = json.loads(body_text or '{}')

        profile, created = Profile.objects.get_or_create(user=request.user)

        # Update user account fields
        if 'username' in data:
            username = data.get('username', '').strip()
            if username and username != request.user.username:
                if User.objects.filter(username=username).exclude(pk=request.user.pk).exists():
                    return JsonResponse({
                        'success': False,
                        'error': 'El nombre de usuario ya está en uso'
                    }, status=400)
                request.user.username = username
                request.user.save()

        if 'name' in data:
            request.user.first_name = data.get('name', request.user.first_name)
            request.user.save()

        # Update profile fields if provided
        if 'display_name' in data:
            profile.display_name = data['display_name']
        if 'ai_name' in data:
            profile.ai_name = data['ai_name']
        if 'profile_background' in data:
            profile.profile_background = data['profile_background']
        if 'app_background' in data:
            profile.app_background = data['app_background']
        if 'screen_appearance' in data:
            profile.screen_appearance = data['screen_appearance']
        if 'font_size' in data:
            profile.font_size = data['font_size']
        if 'theme_preference' in data:
            profile.theme_preference = data['theme_preference']

        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()

        response = {
            'success': True,
            'message': 'Perfil actualizado correctamente',
            'display_name': profile.display_name,
            'username': request.user.username,
            'ai_name': profile.ai_name,
            'profile_background': profile.profile_background,
            'app_background': profile.app_background,
            'screen_appearance': profile.screen_appearance,
            'font_size': profile.font_size,
            'theme_preference': profile.theme_preference,
        }

        if profile.profile_picture:
            response['profile_picture_url'] = profile.profile_picture.url

        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
@require_POST
def logout_view(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('login')

