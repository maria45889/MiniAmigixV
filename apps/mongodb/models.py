from mongoengine import Document, StringField, DateTimeField, IntField, ListField, ReferenceField, FloatField, BooleanField
from datetime import datetime

class ChatMessageMongo(Document):
    """Modelo para almacenar mensajes de chat en MongoDB"""
    usuario = StringField(required=True)
    mensaje = StringField(required=True)
    respuesta = StringField()
    imagen_url = StringField()  # URL de la imagen subida
    fecha_creacion = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'chat_messages',
        'indexes': [
            {'fields': ['usuario'], 'unique': False},
            {'fields': ['fecha_creacion'], 'unique': False}
        ]
    }

class NotificacionMongo(Document):
    """Modelo para almacenar notificaciones en MongoDB"""
    usuario = StringField(required=True)
    titulo = StringField(required=True)
    mensaje = StringField(required=True)
    tipo = StringField()
    leida = IntField(default=0)
    fecha_creacion = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'notificaciones',
        'indexes': [
            {'fields': ['usuario'], 'unique': False},
            {'fields': ['leida'], 'unique': False},
            {'fields': ['fecha_creacion'], 'unique': False}
        ]
    }

class LogActividadMongo(Document):
    """Modelo para almacenar logs de actividad en MongoDB"""
    usuario = StringField(required=True)
    accion = StringField(required=True)
    descripcion = StringField()
    ip_address = StringField()
    fecha_creacion = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'logs_actividad',
        'indexes': [
            {'fields': ['usuario'], 'unique': False},
            {'fields': ['fecha_creacion'], 'unique': False}
        ]
    }

class AnaliticaMongo(Document):
    """Modelo para almacenar datos analíticos en MongoDB"""
    usuario = StringField(required=True)
    pagina = StringField(required=True)
    tiempo_duracion = IntField()
    fecha_creacion = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'analitica',
        'indexes': [
            {'fields': ['usuario'], 'unique': False},
            {'fields': ['pagina'], 'unique': False},
            {'fields': ['fecha_creacion'], 'unique': False}
        ]
    }

# ==================== NUEVOS MODELOS PARA ESTADÍSTICAS Y MÉTRICAS ====================

class EstadisticasUsuarioMongo(Document):
    """Modelo para almacenar estadísticas agregadas por usuario"""
    usuario = StringField(required=True, unique=True)
    total_chats = IntField(default=0)
    total_notificaciones = IntField(default=0)
    total_visitas = IntField(default=0)
    tiempo_total_sesion = IntField(default=0)  # en segundos
    ultima_actividad = DateTimeField(default=datetime.now)
    fecha_creacion = DateTimeField(default=datetime.now)
    fecha_actualizacion = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'estadisticas_usuario',
        'indexes': [
            {'fields': ['usuario'], 'unique': True},
            {'fields': ['ultima_actividad'], 'unique': False}
        ]
    }

class MetricasSistemaMongo(Document):
    """Modelo para almacenar métricas del sistema"""
    fecha = DateTimeField(required=True, unique=True)
    usuarios_activos = IntField(default=0)
    total_chats = IntField(default=0)
    total_notificaciones = IntField(default=0)
    total_visitas = IntField(default=0)
    tiempo_promedio_sesion = FloatField(default=0.0)
    paginas_mas_visitadas = ListField(StringField())
    tasa_retencion = FloatField(default=0.0)
    
    meta = {
        'collection': 'metricas_sistema',
        'indexes': [
            {'fields': ['fecha'], 'unique': True}
        ]
    }

class RendimientoChatMongo(Document):
    """Modelo para almacenar métricas de rendimiento del chat"""
    fecha = DateTimeField(required=True, unique=True)
    total_mensajes = IntField(default=0)
    tiempo_respuesta_promedio = FloatField(default=0.0)  # en segundos
    mensajes_por_usuario = FloatField(default=0.0)
    tasa_error = FloatField(default=0.0)
    tokens_utilizados = IntField(default=0)
    costo_estimado = FloatField(default=0.0)
    
    meta = {
        'collection': 'rendimiento_chat',
        'indexes': [
            {'fields': ['fecha'], 'unique': True}
        ]
    }

class EventoInteraccionMongo(Document):
    """Modelo para almacenar eventos de interacción específicos"""
    usuario = StringField(required=True)
    tipo_evento = StringField(required=True)  # click, scroll, submit, etc.
    elemento = StringField(required=True)  # botón, enlace, formulario, etc.
    pagina = StringField(required=True)
    metadata = StringField()  # datos adicionales en formato JSON
    fecha_creacion = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'eventos_interaccion',
        'indexes': [
            {'fields': ['usuario'], 'unique': False},
            {'fields': ['tipo_evento'], 'unique': False},
            {'fields': ['fecha_creacion'], 'unique': False}
        ]
    }

class SesionUsuarioMongo(Document):
    """Modelo para almacenar sesiones de usuario"""
    usuario = StringField(required=True)
    fecha_inicio = DateTimeField(required=True)
    fecha_fin = DateTimeField()
    duracion = IntField(default=0)  # en segundos
    paginas_visitadas = ListField(StringField())
    acciones_realizadas = ListField(StringField())
    dispositivo = StringField()  # desktop, mobile, tablet
    navegador = StringField()
    ip_address = StringField()
    
    meta = {
        'collection': 'sesiones_usuario',
        'indexes': [
            {'fields': ['usuario'], 'unique': False},
            {'fields': ['fecha_inicio'], 'unique': False}
        ]
    }
