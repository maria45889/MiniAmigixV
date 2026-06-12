from .models import Notificacion

def notificaciones_sin_leer(request):
    if request.user.is_authenticated:
        count = Notificacion.objects.filter(usuario=request.user, leida=False).count()
        return {'notificaciones_sin_leer': count}
    return {'notificaciones_sin_leer': 0}
