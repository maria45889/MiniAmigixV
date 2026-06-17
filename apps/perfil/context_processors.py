from .models import Perfil

def perfil_settings(request):
    if request.user.is_authenticated:
        perfil, _ = Perfil.objects.get_or_create(usuario=request.user)
        return {
            'perfil_tema': perfil.tema,
            'perfil_notificaciones_push': perfil.notificaciones_push,
        }
    return {
        'perfil_tema': 'dark',
        'perfil_notificaciones_push': False,
    }
