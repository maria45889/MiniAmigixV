from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from apps.mongodb.models import (
    ChatMessageMongo, NotificacionMongo, LogActividadMongo, 
    AnaliticaMongo, EstadisticasUsuarioMongo, MetricasSistemaMongo
)
from django.contrib.auth.models import User
from collections import Counter

class Command(BaseCommand):
    help = 'Calcula estadísticas agregadas y las guarda en MongoDB'

    def handle(self, *args, **options):
        self.stdout.write('=== Calculando estadísticas agregadas ===')
        
        # Calcular estadísticas por usuario
        self.stdout.write('\nCalculando estadísticas por usuario...')
        usuarios = User.objects.filter(is_active=True)
        
        for usuario in usuarios:
            try:
                # Obtener datos del usuario
                total_chats = ChatMessageMongo.objects(usuario=usuario.username).count()
                total_notificaciones = NotificacionMongo.objects(usuario=usuario.username).count()
                total_visitas = AnaliticaMongo.objects(usuario=usuario.username).count()
                
                # Calcular tiempo total de sesión (sumando duraciones)
                analiticas = AnaliticaMongo.objects(usuario=usuario.username)
                tiempo_total = sum([a.tiempo_duracion or 0 for a in analiticas])
                
                # Obtener última actividad
                ultimo_log = LogActividadMongo.objects(usuario=usuario.username).order_by('-fecha_creacion').first()
                ultima_actividad = ultimo_log.fecha_creacion if ultimo_log else datetime.now()
                
                # Actualizar o crear estadísticas del usuario
                estadisticas = EstadisticasUsuarioMongo.objects(usuario=usuario.username).first()
                
                if estadisticas:
                    estadisticas.total_chats = total_chats
                    estadisticas.total_notificaciones = total_notificaciones
                    estadisticas.total_visitas = total_visitas
                    estadisticas.tiempo_total_sesion = tiempo_total
                    estadisticas.ultima_actividad = ultima_actividad
                    estadisticas.fecha_actualizacion = datetime.now()
                    estadisticas.save()
                else:
                    estadisticas = EstadisticasUsuarioMongo(
                        usuario=usuario.username,
                        total_chats=total_chats,
                        total_notificaciones=total_notificaciones,
                        total_visitas=total_visitas,
                        tiempo_total_sesion=tiempo_total,
                        ultima_actividad=ultima_actividad,
                        fecha_creacion=datetime.now(),
                        fecha_actualizacion=datetime.now()
                    )
                    estadisticas.save()
                
                self.stdout.write(f'✓ Estadísticas calculadas para: {usuario.username}')
            except Exception as e:
                self.stdout.write(f'✗ Error calculando estadísticas para {usuario.username}: {str(e)}')
        
        # Calcular métricas del sistema
        self.stdout.write('\nCalculando métricas del sistema...')
        try:
            hoy = datetime.now().date()
            fecha_hoy = datetime.combine(hoy, datetime.min.time())
            
            # Usuarios activos (con actividad en los últimos 7 días)
            fecha_limite = datetime.now() - timedelta(days=7)
            usuarios_activos = LogActividadMongo.objects(fecha_creacion__gte=fecha_limite).distinct('usuario')
            total_usuarios_activos = len(usuarios_activos)
            
            # Totales generales
            total_chats = ChatMessageMongo.objects.count()
            total_notificaciones = NotificacionMongo.objects.count()
            total_visitas = AnaliticaMongo.objects.count()
            
            # Tiempo promedio de sesión
            estadisticas_usuarios = EstadisticasUsuarioMongo.objects.all()
            if estadisticas_usuarios.count() > 0:
                tiempo_total = sum([e.tiempo_total_sesion for e in estadisticas_usuarios])
                tiempo_promedio = tiempo_total / estadisticas_usuarios.count()
            else:
                tiempo_promedio = 0.0
            
            # Páginas más visitadas
            paginas = [a.pagina for a in AnaliticaMongo.objects()]
            paginas_contador = Counter(paginas)
            top_paginas = [p[0] for p in paginas_contador.most_common(5)]
            
            # Tasa de retención (usuarios que regresan después de 7 días)
            usuarios_retorno = LogActividadMongo.objects(fecha_creacion__gte=fecha_limite).distinct('usuario')
            tasa_retencion = (len(usuarios_retorno) / usuarios.count()) * 100 if usuarios.count() > 0 else 0
            
            # Guardar métricas del sistema
            metricas = MetricasSistemaMongo.objects(fecha=fecha_hoy).first()
            
            if metricas:
                metricas.usuarios_activos = total_usuarios_activos
                metricas.total_chats = total_chats
                metricas.total_notificaciones = total_notificaciones
                metricas.total_visitas = total_visitas
                metricas.tiempo_promedio_sesion = tiempo_promedio
                metricas.paginas_mas_visitadas = top_paginas
                metricas.tasa_retencion = tasa_retencion
                metricas.save()
            else:
                metricas = MetricasSistemaMongo(
                    fecha=fecha_hoy,
                    usuarios_activos=total_usuarios_activos,
                    total_chats=total_chats,
                    total_notificaciones=total_notificaciones,
                    total_visitas=total_visitas,
                    tiempo_promedio_sesion=tiempo_promedio,
                    paginas_mas_visitadas=top_paginas,
                    tasa_retencion=tasa_retencion
                )
                metricas.save()
            
            self.stdout.write(f'✓ Métricas del sistema calculadas para: {fecha_hoy.strftime("%d/%m/%Y")}')
        except Exception as e:
            self.stdout.write(f'✗ Error calculando métricas del sistema: {str(e)}')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Cálculo de estadísticas completado'))
