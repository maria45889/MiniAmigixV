from django.conf import settings

def site_url(request):
    """
    Context processor para agregar site_url a todas las plantillas
    """
    return {
        'site_url': getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
    }

def user_theme(request):
    """
    Context processor para pasar el tema del usuario a todas las plantillas
    """
    perfil_tema = 'dark'
    perfil_idioma = 'es'
    perfil_nombre_amigis = 'Amigis'
    patito_ropa = 'hoodie'
    patito_color_ropa = 'purple'
    patito_accesorio = 'none'
    patito_color_cuerpo = 'yellow'
    patito_estilo = 'normal'
    perfil_avatar_url = None
    
    if request.user.is_authenticated:
        try:
            from perfil.models import Perfil
            perfil = Perfil.objects.get(usuario=request.user)
            perfil_tema = perfil.tema or 'dark'
            perfil_idioma = perfil.idioma or 'es'
            perfil_nombre_amigis = perfil.nombre_amigis or 'Amigis'
            patito_ropa = perfil.patito_ropa or 'hoodie'
            patito_color_ropa = perfil.patito_color_ropa or 'purple'
            patito_accesorio = perfil.patito_accesorio or 'none'
            patito_color_cuerpo = perfil.patito_color_cuerpo or 'yellow'
            patito_estilo = perfil.patito_estilo or 'normal'
            if perfil.avatar:
                perfil_avatar_url = perfil.avatar.url
        except:
            perfil_tema = 'dark'
            perfil_idioma = 'es'
            perfil_nombre_amigis = 'Amigis'
            patito_ropa = 'hoodie'
            patito_color_ropa = 'purple'
            patito_accesorio = 'none'
            patito_color_cuerpo = 'yellow'
            patito_estilo = 'normal'
    
    return {
        'perfil_tema': perfil_tema,
        'perfil_idioma': perfil_idioma,
        'perfil_nombre_amigis': perfil_nombre_amigis,
        'patito_ropa': patito_ropa,
        'patito_color_ropa': patito_color_ropa,
        'patito_accesorio': patito_accesorio,
        'patito_color_cuerpo': patito_color_cuerpo,
        'patito_estilo': patito_estilo,
        'perfil_avatar_url': perfil_avatar_url
    }

def is_admin_user(request):
    """
    Context processor para verificar si el usuario es admin (solo email en ADMIN_EMAILS)
    """
    allowed_admins = getattr(settings, 'ADMIN_EMAILS', ['miniamigixv@gmail.com'])
    if isinstance(allowed_admins, str):
        allowed_admins = [allowed_admins]
    allowed_admins = [email.strip().lower() for email in allowed_admins if email]
    user_email = (getattr(request.user, 'email', '') or '').strip().lower()
    is_admin = bool(request.user and request.user.is_authenticated and user_email in allowed_admins)
    return {
        'is_admin_user': is_admin
    }
