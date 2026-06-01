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
from django.core.mail import EmailMultiAlternatives, mail_admins, send_mail
from django.contrib.admin.views.decorators import staff_member_required
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from .admin_utils import admin_owner_required
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.template.loader import render_to_string

from datetime import datetime
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
import json
import os
import re
from .models import Profile, SupportTicket, Sugerencia, Notification


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


def clima_api_view(request):
    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse({'error': 'Debe proporcionar una ubicación'}, status=400)

    api_key = getattr(settings, 'OPENWEATHER_API_KEY', '')
    if not api_key:
        return JsonResponse({'error': 'OpenWeather API key no está configurada'}, status=500)

    try:
        geo_url = 'https://api.openweathermap.org/geo/1.0/direct?' + urlencode({'q': q, 'limit': 1, 'appid': api_key})
        req = Request(geo_url, headers={'User-Agent': 'MiniAmigixV/1.0'})
        with urlopen(req, timeout=10) as resp:
            geo_data = json.loads(resp.read().decode('utf-8'))

        if not geo_data:
            return JsonResponse({'error': 'Ubicación no encontrada'}, status=404)

        loc = geo_data[0]
        lat, lon = loc.get('lat'), loc.get('lon')

        weather_url = 'https://api.openweathermap.org/data/2.5/weather?' + urlencode({
            'lat': lat,
            'lon': lon,
            'units': 'metric',
            'lang': 'es',
            'appid': api_key,
        })
        req = Request(weather_url, headers={'User-Agent': 'MiniAmigixV/1.0'})
        with urlopen(req, timeout=10) as resp:
            weather_json = json.loads(resp.read().decode('utf-8'))

        forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?' + urlencode({
            'lat': lat,
            'lon': lon,
            'units': 'metric',
            'lang': 'es',
            'appid': api_key,
        })
        req = Request(forecast_url, headers={'User-Agent': 'MiniAmigixV/1.0'})
        with urlopen(req, timeout=10) as resp:
            forecast_json = json.loads(resp.read().decode('utf-8'))

        data = {
            'name': loc.get('name') or q,
            'country': loc.get('country') or '--',
            'temp': round(weather_json['main']['temp']),
            'feels_like': round(weather_json['main']['feels_like']),
            'humidity': weather_json['main']['humidity'],
            'pressure': weather_json['main']['pressure'],
            'wind_speed': weather_json['wind']['speed'],
            'visibility': weather_json.get('visibility', 10000),
            'description': weather_json['weather'][0]['description'],
            'icon': weather_json['weather'][0]['icon'],
            'rain': (weather_json.get('rain', {}).get('1h', 0) or weather_json.get('rain', {}).get('3h', 0) or 0)
                + (weather_json.get('snow', {}).get('1h', 0) or weather_json.get('snow', {}).get('3h', 0) or 0),
            'sunrise': weather_json['sys']['sunrise'],
            'sunset': weather_json['sys']['sunset'],
            'forecast': [],
        }

        if forecast_json and forecast_json.get('list'):
            by_day = {}
            for item in forecast_json['list']:
                day = datetime.fromtimestamp(item['dt']).strftime('%d/%m/%Y')
                by_day.setdefault(day, []).append(item)

            days = list(by_day.keys())[:5]
            for d in days:
                items = by_day[d]
                temps = [i['main']['temp'] for i in items]
                min_temp = int(min(temps))
                max_temp = int(max(temps))
                desc = items[0]['weather'][0]['description']
                icon = items[0]['weather'][0]['icon']
                rain_volume = sum(
                    (i.get('rain', {}).get('3h', 0) or 0) + (i.get('snow', {}).get('3h', 0) or 0)
                    for i in items
                )
                data['forecast'].append({
                    'day': datetime.fromtimestamp(items[0]['dt']).strftime('%a'),
                    'date': d,
                    'temp_min': min_temp,
                    'temp_max': max_temp,
                    'description': desc,
                    'icon': icon,
                    'rain': rain_volume,
                })

        return JsonResponse(data)

    except HTTPError as err:
        return JsonResponse({'error': 'Error de OpenWeather: ' + str(err)}, status=502)
    except URLError as err:
        return JsonResponse({'error': 'No se pudo conectar con OpenWeather', 'details': str(err)}, status=502)
    except Exception as err:
        return JsonResponse({'error': 'Error interno al obtener el clima', 'details': str(err)}, status=500)


@require_POST
def traductor_translate(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'success': False, 'error': 'Solicitud inválida'}, status=400)

    text = payload.get('text', '').strip()
    source = payload.get('source', 'auto')
    target = payload.get('target', 'es')

    if not text:
        return JsonResponse({'success': False, 'error': 'Texto vacío'}, status=400)

    detected_source = source
    if source == 'auto':
        spanish_clues = ['que', 'cómo', 'por qué', 'dónde', 'hola', 'gracias', 'usted', 'está', 'muy', 'sí', 'adiós']
        lower_text = text.lower()
        if re.search(r'[áéíóúñ¿¡]', text, re.IGNORECASE) or any(clue in lower_text for clue in spanish_clues):
            detected_source = 'es'
        else:
            detected_source = 'en'

    translated_text = f"[Traducción simulada de {detected_source} a {target}]\n\n{text}"

    return JsonResponse({
        'success': True,
        'translated_text': translated_text,
        'source': detected_source,
        'mock': True
    })


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

        # Prepare context for HTML emails
        now = timezone.localtime(timezone.now())
        autor_nombre = request.user.get_full_name() or request.user.username
        autor_email = request.user.email or '(sin email)'

        # Function to send HTML email for new support ticket notification to admins
        def enviar_notificacion_nuevo_soporte(ticket):
            subject = f"[Soporte MiniAmigixV] Nuevo ticket: {ticket.title}"
            context = {
                'usuario_nombre': autor_nombre,
                'usuario_email': autor_email,
                'fecha_hora': now.strftime('%d/%m/%Y %H:%M'),
                'tipo_display': ticket.get_tipo_display(),
                'tipo_clase': ticket.tipo.lower(),
                'prioridad_display': ticket.get_prioridad_display(),
                'prioridad_clase': ticket.prioridad.lower(),
                'estado_display': ticket.get_estado_display(),
                'estado_clase': ticket.estado.lower(),
                'descripcion': ticket.description,
                'ticket_id': ticket.id,
                'año': now.year,
            }

            try:
                html_content = render_to_string('emails/nuevo_soporte.html', context)
                
                # Send to admins
                admin_emails = [admin[1] for admin in settings.ADMINS] if settings.ADMINS else [settings.ADMIN_EMAIL]
                if not admin_emails:
                    admin_emails = [settings.DEFAULT_FROM_EMAIL.split('<')[1].strip('>') if '<' in settings.DEFAULT_FROM_EMAIL else settings.DEFAULT_FROM_EMAIL]
                
                msg = EmailMultiAlternatives(
                    subject,
                    '',  # Versión de texto plano (vacía, solo usamos HTML)
                    settings.DEFAULT_FROM_EMAIL,
                    admin_emails
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except Exception as e:
                # Fallback to plain text if HTML fails
                message = (
                    "Se ha creado un nuevo ticket de soporte desde la plataforma MiniAmigixV.\n\n"
                    f"Usuario: {autor_nombre} <{autor_email}>\n"
                    f"Tipo: {ticket.get_tipo_display()}\n"
                    f"Prioridad: {ticket.get_prioridad_display()}\n"
                    f"Estado: {ticket.get_estado_display()}\n"
                    f"Fecha y hora: {now.strftime('%d/%m/%Y %H:%M')}\n\n"
                    f"Descripción:\n{ticket.description}\n"
                )
                try:
                    mail_admins(subject, message, fail_silently=False)
                except Exception:
                    pass  # Silently fail to not break the flow

        # Function to send HTML email for support ticket confirmation to user
        def enviar_confirmacion_soporte_usuario(ticket):
            user_subject = f"[MiniAmigixV] Confirmación de tu ticket: {ticket.title}"
            context = {
                'autor_nombre': autor_nombre,
                'autor_email': autor_email,
                'ticket_titulo': ticket.title,
                'tipo_display': ticket.get_tipo_display(),
                'tipo_clase': ticket.tipo.lower(),
                'prioridad_display': ticket.get_prioridad_display(),
                'prioridad_clase': ticket.prioridad.lower(),
                'estado_display': ticket.get_estado_display(),
                'estado_clase': ticket.estado.lower(),
                'fecha_envio': now.strftime('%d/%m/%Y %H:%M'),
                'descripcion': ticket.description,
                'soporte_url': request.build_absolute_uri(reverse('soporte')),
                'año': now.year,
            }

            try:
                html_content = render_to_string('emails/nuevo_soporte.html', context)
                
                if request.user.email:
                    msg = EmailMultiAlternatives(
                        user_subject,
                        '',  # Versión de texto plano (vacía, solo usamos HTML)
                        settings.DEFAULT_FROM_EMAIL,
                        [request.user.email]
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
            except Exception as e:
                # Fallback to plain text if HTML fails
                user_message = (
                    f"Hola {autor_nombre},\n\n"
                    "Recibimos tu solicitud de soporte y el equipo de MiniAmigixV ya fue notificado.\n\n"
                    f"Título: {ticket.title}\n"
                    f"Tipo: {ticket.get_tipo_display()}\n"
                    f"Prioridad: {ticket.get_prioridad_display()}\n"
                    f"Creado en: {now.strftime('%d/%m/%Y %H:%M')}\n\n"
                    "Cuando el administrador responda, también recibirás un correo con la respuesta.\n\n"
                    "Gracias por usar MiniAmigixV."
                )
                try:
                    if request.user.email:
                        send_mail(
                            user_subject,
                            user_message,
                            settings.DEFAULT_FROM_EMAIL,
                            [request.user.email],
                            fail_silently=False,
                        )
                except Exception:
                    pass  # Silently fail to not break the flow

        try:
            # 1) Notificar al admin (HTML)
            enviar_notificacion_nuevo_soporte(ticket)

            # 2) Acuse/confirmación al usuario por correo (HTML)
            enviar_confirmacion_soporte_usuario(ticket)

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
            # Send HTML email for support ticket response
            now = timezone.localtime(timezone.now())
            autor_nombre = ticket.user.get_full_name() or ticket.user.username
            
            subject = f"Respuesta a tu ticket de soporte: {ticket.title}"
            context = {
                'autor_nombre': autor_nombre,
                'autor_email': ticket.user.email or '(sin email)',
                'ticket_titulo': ticket.title,
                'tipo_display': ticket.get_tipo_display(),
                'tipo_clase': ticket.tipo.lower(),
                'prioridad_display': ticket.get_prioridad_display(),
                'prioridad_clase': ticket.prioridad.lower(),
                'estado_original_display': ticket.get_estado_display(),  # Before change
                'estado_original_clase': ticket.estado.lower(),  # Before change (will update after)
                'fecha_envio': ticket.created_at.strftime('%d/%m/%Y %H:%M'),
                'respuesta': ticket.respuesta,
                'respondido_por': request.user.get_full_name() or request.user.username,
                'fecha_respuesta': now.strftime('%d/%m/%Y %H:%M'),
                'estado_actual_display': estado,  # The new estado being set
                'estado_actual_clase': estado.lower(),
                'ticket_id': ticket.id,
                'soporte_url': request.build_absolute_uri(reverse('soporte')),
                'año': now.year,
            }

            try:
                html_content = render_to_string('emails/respuesta_soporte.html', context)
                
                msg = EmailMultiAlternatives(
                    subject,
                    '',  # Versión de texto plano (vacía, solo usamos HTML)
                    settings.DEFAULT_FROM_EMAIL,
                    [ticket.user.email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except Exception as e:
                # Fallback to plain text if HTML fails
                message = (
                    f"Hola {autor_nombre},\n\n"
                    f"Tu solicitud de soporte ha recibido una respuesta del administrador.\n\n"
                    f"Título: {ticket.title}\n"
                    f"Tipo: {ticket.get_tipo_display()}\n"
                    f"Prioridad: {ticket.get_prioridad_display()}\n"
                    f"Estado: {estado}\n\n"
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
                    pass  # Silently fail to not break the flow

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
    
    # Preparar contexto para el template HTML
    admin_url = request.build_absolute_uri(f'/admin/users/sugerencia/{sugerencia.id}/change/')

    context = {
        'autor_nombre': autor_nombre,
        'autor_email': autor_email,
        'fecha_hora': now.strftime('%d/%m/%Y %H:%M'),
        'tipo_display': sugerencia.get_tipo_display(),
        'tipo_clase': sugerencia.tipo.lower(),  # Para las clases CSS
        'estado_display': sugerencia.get_estado_display(),
        'estado_clase': sugerencia.estado.lower(),  # Para las clases CSS
        'descripcion': sugerencia.descripcion,
        'sugerencia_id': sugerencia.id,
        'admin_url': admin_url,
        'año': now.year,
    }

    try:
        # Intentar enviar correo HTML
        from django.core.mail import EmailMultiAlternatives
        from django.template.loader import render_to_string
        
        html_content = render_to_string('emails/nueva_sugerencia.html', context)
        
        msg = EmailMultiAlternatives(
            subject,
            'Nueva sugerencia recibida en MiniAmigixV. Abre este correo en un cliente con soporte HTML para ver el mensaje completo.',
            remitente,
            destino
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        # Fallback a texto plano si falla el HTML
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


@login_required
def notificaciones_view(request):
    """View notifications with pagination"""
    # Get user notifications
    notificaciones = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notificaciones.filter(is_read=False).count()
    
    # Pagination
    paginator = Paginator(notificaciones, 15)  # 15 notificaciones por página
    page_number = request.GET.get('page')
    notifications = paginator.get_page(page_number)
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'notificaciones/index.html', context)


def panel_dashboard(request):
    """Custom helpdesk dashboard panel"""
    # Restrict to staff/admin users only
    if not request.user.is_staff:
        messages.error(request, 'No tienes permiso para acceder al panel de administración.')
        return redirect('home')
    
    # Get statistics
    total_sugerencias = Sugerencia.objects.count()
    sugerencias_pendientes = Sugerencia.objects.filter(estado='pendiente').count()
    sugerencias_en_revision = Sugerencia.objects.filter(estado='en_revision').count()
    sugerencias_resueltas = Sugerencia.objects.filter(estado__in=['respuesta', 'resuelta']).count()
    
    total_soportes = SupportTicket.objects.count()
    soportes_abiertos = SupportTicket.objects.filter(estado='abierto').count()
    soportes_en_revision = SupportTicket.objects.filter(estado='en_revision').count()
    soportes_resueltos = SupportTicket.objects.filter(estado='resuelto').count()
    
    # Recent items (last 10)
    recent_sugerencias = Sugerencia.objects.select_related('user').order_by('-created_at')[:10]
    recent_soportes = SupportTicket.objects.select_related('user').order_by('-created_at')[:10]
    
    # Tipo distribution for charts
    sugerencia_tipos = Sugerencia.objects.values('tipo').annotate(count=Count('tipo')).order_by('-count')
    soporte_tipos = SupportTicket.objects.values('tipo').annotate(count=Count('tipo')).order_by('-count')
    
    # Prioridad distribution for soporte tickets
    soporte_prioridades = SupportTicket.objects.values('prioridad').annotate(count=Count('prioridad')).order_by('-count')
    
    context = {
        'total_sugerencias': total_sugerencias,
        'sugerencias_pendientes': sugerencias_pendientes,
        'sugerencias_en_revision': sugerencias_en_revision,
        'sugerencias_resueltas': sugerencias_resueltas,
        'total_soportes': total_soportes,
        'soportes_abiertos': soportes_abiertos,
        'soportes_en_revision': soportes_en_revision,
        'soportes_resueltos': soportes_resueltos,
        'recent_sugerencias': recent_sugerencias,
        'recent_soportes': recent_soportes,
        'sugerencia_tipos': list(sugerencia_tipos),
        'soporte_tipos': list(soporte_tipos),
        'soporte_prioridades': list(soporte_prioridades),
    }
    
    return render(request, 'panel/dashboard.html', context)


def bandeja_sugerencias(request):
    """Inbox-style view for managing suggestions"""
    # Restrict to staff/admin users only
    if not request.user.is_staff:
        messages.error(request, 'No tienes permiso para acceder al panel de administración.')
        return redirect('home')
    
    # Get filter parameters
    estado_filtro = request.GET.get('estado', '')
    tipo_filtro = request.GET.get('tipo', '')
    busqueda = request.GET.get('q', '')
    
    # Base queryset
    sugerencias = Sugerencia.objects.select_related('user', 'respondido_por').all()
    
    # Apply filters
    if estado_filtro:
        sugerencias = sugerencias.filter(estado=estado_filtro)
    if tipo_filtro:
        sugerencias = sugerencias.filter(tipo=tipo_filtro)
    if busqueda:
        sugerencias = sugerencias.filter(
            Q(titulo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(user__username__icontains=busqueda) |
            Q(user__email__icontains=busqueda)
        )
    
    # Order by most recent first
    sugerencias = sugerencias.order_by('-created_at')
    
    # Get statistics for the filter badges
    stats = {
        'total': Sugerencia.objects.count(),
        'pendiente': Sugerencia.objects.filter(estado='pendiente').count(),
        'en_revision': Sugerencia.objects.filter(estado='en_revision').count(),
        'respuesta': Sugerencia.objects.filter(estado='respuesta').count(),
        'resuelta': Sugerencia.objects.filter(estado='resuelta').count(),
    }
    
    # Get filter options
    tipo_choices = Sugerencia.TIPO_CHOICES
    estado_choices = Sugerencia.ESTADO_CHOICES
    
    context = {
        'sugerencias': sugerencias,
        'stats': stats,
        'tipo_choices': tipo_choices,
        'estado_choices': estado_choices,
        'current_estado': estado_filtro,
        'current_tipo': tipo_filtro,
        'current_busqueda': busqueda,
    }
    
    return render(request, 'panel/bandeja_sugerencias.html', context)


def bandeja_soporte(request):
    """Inbox-style view for managing support tickets"""
    # Restrict to staff/admin users only
    if not request.user.is_staff:
        messages.error(request, 'No tienes permiso para acceder al panel de administración.')
        return redirect('home')
    
    # Get filter parameters
    estado_filtro = request.GET.get('estado', '')
    tipo_filtro = request.GET.get('tipo', '')
    prioridad_filtro = request.GET.get('prioridad', '')
    busqueda = request.GET.get('q', '')
    
    # Base queryset
    tickets = SupportTicket.objects.select_related('user', 'respondido_por').all()
    
    # Apply filters
    if estado_filtro:
        tickets = tickets.filter(estado=estado_filtro)
    if tipo_filtro:
        tickets = tickets.filter(tipo=tipo_filtro)
    if prioridad_filtro:
        tickets = tickets.filter(prioridad=prioridad_filtro)
    if busqueda:
        tickets = tickets.filter(
            Q(title__icontains=busqueda) |
            Q(description__icontains=busqueda) |
            Q(user__username__icontains=busqueda) |
            Q(user__email__icontains=busqueda)
        )
    
    # Order by most recent first
    tickets = tickets.order_by('-created_at')
    
    # Get statistics for the filter badges
    stats = {
        'total': SupportTicket.objects.count(),
        'abierto': SupportTicket.objects.filter(estado='abierto').count(),
        'en_revision': SupportTicket.objects.filter(estado='en_revision').count(),
        'resuelto': SupportTicket.objects.filter(estado='resuelto').count(),
    }
    
    # Get filter options
    tipo_choices = SupportTicket.TIPO_CHOICES
    estado_choices = SupportTicket.ESTADO_CHOICES
    prioridad_choices = SupportTicket.PRIORIDAD_CHOICES
    
    context = {
        'tickets': tickets,
        'stats': stats,
        'tipo_choices': tipo_choices,
        'estado_choices': estado_choices,
        'prioridad_choices': prioridad_choices,
        'current_estado': estado_filtro,
        'current_tipo': tipo_filtro,
        'current_prioridad': prioridad_filtro,
        'current_busqueda': busqueda,
    }
    
    return render(request, 'panel/bandeja_soporte.html', context)


def responder_sugerencia(request, sugerencia_id):
    """Handle AJAX response to a suggestion from the inbox view"""
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    try:
        sugerencia = Sugerencia.objects.get(id=sugerencia_id)
    except Sugerencia.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Suggestion not found'}, status=404)
    
    respuesta_text = request.POST.get('respuesta', '').strip()
    nuevo_estado = request.POST.get('nuevo_estado', sugerencia.estado)
    
    if not respuesta_text:
        return JsonResponse({'success': False, 'error': 'Response text is required'}, status=400)
    
    # Update the suggestion
    sugerencia.respuesta = respuesta_text
    sugerencia.respondido_por = request.user
    sugerencia.respondido_en = timezone.now()
    if nuevo_estado in dict(Sugerencia.ESTADO_CHOICES):
        sugerencia.estado = nuevo_estado
    sugerencia.save()
    
    # Create notification for user
    Notification.objects.create(
        user=sugerencia.user,
        title=f"Respuesta a tu sugerencia: {sugerencia.titulo[:100]}",
        message=respuesta_text[:200],
        notification_type='sugerencia_respuesta',
        related_url=f'/sugerencias/',
        related_object_id=sugerencia.id
    )
    
    # Send email notification to the user
    try:
        # Reuse the email sending logic from admin
        now = timezone.localtime(timezone.now())
        autor_nombre = sugerencia.user.get_full_name() or sugerencia.user.username
        autor_email = sugerencia.user.email or '(sin email)'
        
        subject = f"[MiniAmigixV] Respuesta a tu sugerencia: {sugerencia.titulo}"
        context = {
            'autor_nombre': autor_nombre,
            'autor_email': autor_email,
            'sugerencia_titulo': sugerencia.titulo,
            'tipo_display': sugerencia.get_tipo_display(),
            'tipo_clase': sugerencia.tipo.lower(),
            'estado_original_display': sugerencia.get_estado_display(),
            'estado_original_clase': sugerencia.estado.lower(),
            'fecha_envio': sugerencia.created_at.strftime('%d/%m/%Y %H:%M'),
            'respuesta': sugerencia.respuesta,
            'respondido_por': sugerencia.respondido_por.get_full_name() or sugerencia.respondido_por.username if sugerencia.respondido_por else 'Equipo',
            'fecha_respuesta': now.strftime('%d/%m/%Y %H:%M'),
            'estado_actual_display': sugerencia.get_estado_display(),
            'estado_actual_clase': sugerencia.estado.lower(),
            'sugerencia_id': sugerencia.id,
            'sugerencias_url': request.build_absolute_uri(reverse('sugerencias')),
            'año': now.year,
        }

        html_content = render_to_string('emails/respuesta_sugerencia.html', context)
        
        msg = EmailMultiAlternatives(
            subject,
            'Tu sugerencia ha sido respondida. Abre este correo en un cliente con soporte HTML para ver el mensaje completo.',
            settings.DEFAULT_FROM_EMAIL,
            [sugerencia.user.email] if sugerencia.user.email else []
        )
        if sugerencia.user.email:
            msg.attach_alternative(html_content, "text/html")
            msg.send()
    except Exception:
        # Silently fail to not break the response if email fails
        pass
    
    return JsonResponse({'success': True, 'message': 'Response sent successfully'})


def responder_soporte(request, ticket_id):
    """Handle AJAX response to a support ticket from the inbox view"""
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    try:
        ticket = SupportTicket.objects.get(id=ticket_id)
    except SupportTicket.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Ticket not found'}, status=404)
    
    respuesta_text = request.POST.get('respuesta', '').strip()
    nuevo_estado = request.POST.get('nuevo_estado', ticket.estado)
    
    if not respuesta_text:
        return JsonResponse({'success': False, 'error': 'Response text is required'}, status=400)
    
    # Update the ticket
    ticket.respuesta = respuesta_text
    ticket.respondido_por = request.user
    ticket.respondido_en = timezone.now()
    if nuevo_estado in dict(SupportTicket.ESTADO_CHOICES):
        ticket.estado = nuevo_estado
    ticket.save()
    
    # Create notification for user
    Notification.objects.create(
        user=ticket.user,
        title=f"Respuesta a tu ticket de soporte: {ticket.title[:100]}",
        message=respuesta_text[:200],
        notification_type='soporte_respuesta',
        related_url=f'/soporte/',
        related_object_id=ticket.id
    )
    
    # Send email notification to the user
    try:
        now = timezone.localtime(timezone.now())
        autor_nombre = ticket.user.get_full_name() or ticket.user.username
        
        subject = f"Respuesta a tu ticket de soporte: {ticket.title}"
        context = {
            'autor_nombre': autor_nombre,
            'autor_email': ticket.user.email or '(sin email)',
            'ticket_titulo': ticket.title,
            'tipo_display': ticket.get_tipo_display(),
            'tipo_clase': ticket.tipo.lower(),
            'prioridad_display': ticket.get_prioridad_display(),
            'prioridad_clase': ticket.prioridad.lower(),
            'estado_original_display': ticket.get_estado_display(),
            'estado_original_clase': ticket.estado.lower(),
            'fecha_envio': ticket.created_at.strftime('%d/%m/%Y %H:%M'),
            'respuesta': ticket.respuesta,
            'respondido_por': request.user.get_full_name() or request.user.username,
            'fecha_respuesta': now.strftime('%d/%m/%Y %H:%M'),
            'estado_actual_display': nuevo_estado,
            'estado_actual_clase': nuevo_estado.lower(),
            'ticket_id': ticket.id,
            'año': now.year,
        }

        html_content = render_to_string('emails/respuesta_soporte.html', context)
        
        msg = EmailMultiAlternatives(
            subject,
            '',  # Versión de texto plano (vacía, solo usamos HTML)
            settings.DEFAULT_FROM_EMAIL,
            [ticket.user.email] if ticket.user.email else []
        )
        if ticket.user.email:
            msg.attach_alternative(html_content, "text/html")
            msg.send()
    except Exception:
        # Silently fail to not break the response if email fails
        pass
    
    return JsonResponse({'success': True, 'message': 'Response sent successfully'})

