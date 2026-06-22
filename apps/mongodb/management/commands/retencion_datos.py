from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from apps.mongodb.models import (
    ChatMessageMongo, NotificacionMongo, LogActividadMongo, 
    AnaliticaMongo, EventoInteraccionMongo
)

class Command(BaseCommand):
    help = 'Implementa sistema de retención de datos eliminando registros antiguos'

    def handle(self, *args, **options):
        self.stdout.write('=== Sistema de Retención de Datos ===')
        
        # Configuración de retención (en días)
        retencion_config = {
            'chat_messages': 90,      # 90 días para mensajes de chat
            'notificaciones': 30,    # 30 días para notificaciones
            'logs_actividad': 60,    # 60 días para logs de actividad
            'analitica': 30,         # 30 días para datos analíticos
            'eventos_interaccion': 45 # 45 días para eventos de interacción
        }
        
        total_eliminados = 0
        
        # Eliminar mensajes de chat antiguos
        self.stdout.write('\n1. Limpiando mensajes de chat antiguos...')
        fecha_limite_chat = datetime.now() - timedelta(days=retencion_config['chat_messages'])
        chats_eliminados = ChatMessageMongo.objects(fecha_creacion__lt=fecha_limite_chat).delete()
        total_eliminados += chats_eliminados if chats_eliminados else 0
        self.stdout.write(f'   ✓ {chats_eliminados if chats_eliminados else 0} mensajes de chat eliminados (más de {retencion_config["chat_messages"]} días)')
        
        # Eliminar notificaciones antiguas
        self.stdout.write('\n2. Limpiando notificaciones antiguas...')
        fecha_limite_notif = datetime.now() - timedelta(days=retencion_config['notificaciones'])
        notifs_eliminadas = NotificacionMongo.objects(fecha_creacion__lt=fecha_limite_notif).delete()
        total_eliminados += notifs_eliminadas if notifs_eliminadas else 0
        self.stdout.write(f'   ✓ {notifs_eliminadas if notifs_eliminadas else 0} notificaciones eliminadas (más de {retencion_config["notificaciones"]} días)')
        
        # Eliminar logs de actividad antiguos
        self.stdout.write('\n3. Limpiando logs de actividad antiguos...')
        fecha_limite_logs = datetime.now() - timedelta(days=retencion_config['logs_actividad'])
        logs_eliminados = LogActividadMongo.objects(fecha_creacion__lt=fecha_limite_logs).delete()
        total_eliminados += logs_eliminados if logs_eliminados else 0
        self.stdout.write(f'   ✓ {logs_eliminados if logs_eliminados else 0} logs de actividad eliminados (más de {retencion_config["logs_actividad"]} días)')
        
        # Eliminar datos analíticos antiguos
        self.stdout.write('\n4. Limpiando datos analíticos antiguos...')
        fecha_limite_analitica = datetime.now() - timedelta(days=retencion_config['analitica'])
        analitica_eliminada = AnaliticaMongo.objects(fecha_creacion__lt=fecha_limite_analitica).delete()
        total_eliminados += analitica_eliminada if analitica_eliminada else 0
        self.stdout.write(f'   ✓ {analitica_eliminada if analitica_eliminada else 0} registros analíticos eliminados (más de {retencion_config["analitica"]} días)')
        
        # Eliminar eventos de interacción antiguos
        self.stdout.write('\n5. Limpiando eventos de interacción antiguos...')
        fecha_limite_eventos = datetime.now() - timedelta(days=retencion_config['eventos_interaccion'])
        eventos_eliminados = EventoInteraccionMongo.objects(fecha_creacion__lt=fecha_limite_eventos).delete()
        total_eliminados += eventos_eliminados if eventos_eliminados else 0
        self.stdout.write(f'   ✓ {eventos_eliminados if eventos_eliminados else 0} eventos de interacción eliminados (más de {retencion_config["eventos_interaccion"]} días)')
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Sistema de retención completado. Total eliminados: {total_eliminados} registros'))
        
        # Mostrar estadísticas actuales
        self.stdout.write('\n=== Estadísticas Actuales ===')
        self.stdout.write(f'Mensajes de chat: {ChatMessageMongo.objects.count()}')
        self.stdout.write(f'Notificaciones: {NotificacionMongo.objects.count()}')
        self.stdout.write(f'Logs de actividad: {LogActividadMongo.objects.count()}')
        self.stdout.write(f'Datos analíticos: {AnaliticaMongo.objects.count()}')
        self.stdout.write(f'Eventos de interacción: {EventoInteraccionMongo.objects.count()}')
