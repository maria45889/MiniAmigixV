from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.mongodb.models import ChatMessageMongo, NotificacionMongo, LogActividadMongo, AnaliticaMongo
from apps.mongodb.services import DualDatabaseService
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from collections import Counter

@login_required
def dashboard_analitica(request):
    """Dashboard de analítica con datos de MongoDB"""
    
    # Obtener estadísticas generales
    stats_generales = {
        'total_chats': ChatMessageMongo.objects.count(),
        'total_notificaciones': NotificacionMongo.objects.count(),
        'total_logs': LogActividadMongo.objects.count(),
        'total_analitica': AnaliticaMongo.objects.count(),
        'total_usuarios': User.objects.filter(is_active=True).count()
    }
    
    # Obtener estadísticas del usuario actual
    if request.user.is_authenticated:
        stats_usuario = DualDatabaseService.obtener_estadisticas_usuario(request.user.username)
    else:
        stats_usuario = {}
    
    # Obtener actividad reciente (últimos 7 días)
    fecha_limite = datetime.now() - timedelta(days=7)
    actividad_reciente = LogActividadMongo.objects(fecha_creacion__gte=fecha_limite).order_by('-fecha_creacion')[:20]
    
    # Obtener chats más activos
    chats_por_usuario = Counter([chat.usuario for chat in ChatMessageMongo.objects])
    top_usuarios_chats = chats_por_usuario.most_common(5)
    
    # Obtener páginas más visitadas
    paginas_visitadas = Counter([analitica.pagina for analitica in AnaliticaMongo.objects])
    top_paginas = paginas_visitadas.most_common(5)
    
    # Obtener notificaciones por tipo
    notificaciones_por_tipo = Counter([notif.tipo for notif in NotificacionMongo.objects])
    
    context = {
        'stats_generales': stats_generales,
        'stats_usuario': stats_usuario,
        'actividad_reciente': actividad_reciente,
        'top_usuarios_chats': top_usuarios_chats,
        'top_paginas': top_paginas,
        'notificaciones_por_tipo': dict(notificaciones_por_tipo),
    }
    
    return render(request, 'mongodb/dashboard_analitica.html', context)
