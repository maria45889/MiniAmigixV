from django.shortcuts import render, redirect
from .models import Perfil, UserActivity, UserProfileAchievement
from django.contrib.auth.models import User
from django.utils import timezone
from apps.notificaciones.models import Notificacion
from apps.eventos.models import Evento
from apps.app.models import ConversacionChat, Cancion, Score

def ver_perfil(request):
    if request.user.is_authenticated:
        perfil, created = Perfil.objects.get_or_create(usuario=request.user)
        try:
            total_notificaciones = Notificacion.objects.filter(usuario=request.user).count()
            total_eventos = Evento.objects.filter(usuario=request.user).count()
            total_chats = ConversacionChat.objects.filter(usuario=request.user).count()
            total_canciones = Cancion.objects.filter(usuario=request.user).count()
            total_juegos = Score.objects.filter(usuario=request.user).count()
            actividades_recientes = UserActivity.objects.filter(usuario=request.user)[:5]
            logros_desbloqueados = UserProfileAchievement.objects.filter(usuario=request.user).select_related('logro')
        except Exception:
            total_notificaciones = 0
            total_eventos = 0
            total_chats = 0
            total_canciones = 0
            total_juegos = 0
            actividades_recientes = []
            logros_desbloqueados = []
            
        if perfil.creado:
            dias_activo = (timezone.now().date() - perfil.creado.date()).days
        else:
            dias_activo = 0
        
        # Calcular progreso de nivel
        if perfil.experiencia_siguiente_nivel > 0:
            progreso_nivel = int((perfil.experiencia / perfil.experiencia_siguiente_nivel) * 100)
        else:
            progreso_nivel = 0
            
        return render(request, 'perfil/index.html', {
            'perfil': perfil,
            'total_notificaciones': total_notificaciones,
            'total_eventos': total_eventos,
            'total_chats': total_chats,
            'total_canciones': total_canciones,
            'total_juegos': total_juegos,
            'dias_activo': dias_activo,
            'actividades_recientes': actividades_recientes,
            'logros_desbloqueados': logros_desbloqueados,
            'progreso_nivel': progreso_nivel,
        })
    else:
        return render(request, 'perfil/index.html', {'perfil': None})

def editar_perfil(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        try:
            # Guardar todos los campos del POST
            for field in ['bio', 'tema', 'idioma', 'ubicacion', 'color_acento', 'nombre_amigis',
                         'patito_ropa', 'patito_color_ropa', 'patito_accesorio', 'patito_color_cuerpo', 'patito_estilo',
                         'formato_reloj', 'zona_horaria']:
                value = request.POST.get(field, '')
                if value:
                    setattr(perfil, field, value)
            
            # Fecha de nacimiento
            fecha_nacimiento = request.POST.get('fecha_nacimiento', '').strip()
            if fecha_nacimiento:
                perfil.fecha_nacimiento = fecha_nacimiento
            
            # Avatar
            if 'avatar' in request.FILES and request.FILES['avatar']:
                perfil.avatar = request.FILES['avatar']
            
            perfil.save()
            
            from django.contrib import messages
            messages.success(request, '¡Perfil actualizado correctamente!')
            return redirect('perfil')
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'perfil/editar.html', {'perfil': perfil})
