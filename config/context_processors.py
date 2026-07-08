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
    if request.user.is_authenticated:
        try:
            from perfil.models import Perfil
            perfil = Perfil.objects.get(usuario=request.user)
            perfil_tema = perfil.tema or 'dark'
            perfil_idioma = perfil.idioma or 'es'
        except:
            perfil_tema = 'dark'
            perfil_idioma = 'es'
    
    return {
        'perfil_tema': perfil_tema,
        'perfil_idioma': perfil_idioma
    }

def is_admin_user(request):
    """
    Context processor para verificar si el usuario es admin (solo email en ADMIN_EMAILS)
    """
    from apps.app.views import is_admin_user as check_admin
    return {
        'is_admin_user': check_admin(request.user)
    }
