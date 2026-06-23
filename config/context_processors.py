from django.conf import settings

def site_url(request):
    """
    Context processor para agregar site_url a todas las plantillas
    """
    return {
        'site_url': getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
    }
