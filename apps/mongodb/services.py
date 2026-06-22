from apps.mongodb.models import ChatMessageMongo, NotificacionMongo, LogActividadMongo, AnaliticaMongo, EventoInteraccionMongo
from app.models import MensajeChat
from notificaciones.models import Notificacion
from datetime import datetime

class DualDatabaseService:
    """Servicio para gestionar el sistema dual de bases de datos (SQLite + MongoDB)"""
    
    @staticmethod
    def guardar_chat_mensaje(usuario, mensaje, respuesta=None, usar_mongodb=True):
        """
        Guarda mensaje de chat en ambas bases de datos
        - SQLite: Para datos críticos y relaciones
        - MongoDB: Para historial y análisis
        """
        # Guardar en SQLite (crítico)
        # Esto ya se hace en el views.py de app
        
        # Guardar en MongoDB (historial y análisis)
        if usar_mongodb:
            try:
                chat_mongo = ChatMessageMongo(
                    usuario=usuario,
                    mensaje=mensaje,
                    respuesta=respuesta,
                    fecha_creacion=datetime.now()
                )
                chat_mongo.save()
                return chat_mongo.id
            except Exception as e:
                print(f"Error guardando en MongoDB: {str(e)}")
        return None
    
    @staticmethod
    def guardar_notificacion(usuario, titulo, mensaje, tipo='info', usar_mongodb=True):
        """
        Guarda notificación en ambas bases de datos
        - SQLite: Para notificaciones activas y gestión
        - MongoDB: Para historial y análisis
        """
        # Guardar en SQLite (crítico)
        # Esto ya se hace en el views.py correspondiente
        
        # Guardar en MongoDB (historial y análisis)
        if usar_mongodb:
            try:
                notif_mongo = NotificacionMongo(
                    usuario=usuario,
                    titulo=titulo,
                    mensaje=mensaje,
                    tipo=tipo,
                    leida=0,
                    fecha_creacion=datetime.now()
                )
                notif_mongo.save()
                return notif_mongo.id
            except Exception as e:
                print(f"Error guardando en MongoDB: {str(e)}")
        return None
    
    @staticmethod
    def log_actividad(usuario, accion, descripcion=None, ip_address=None):
        """
        Registra actividad solo en MongoDB
        - MongoDB: Para logs y análisis de actividad
        """
        try:
            log = LogActividadMongo(
                usuario=usuario,
                accion=accion,
                descripcion=descripcion,
                ip_address=ip_address,
                fecha_creacion=datetime.now()
            )
            log.save()
            return log.id
        except Exception as e:
            print(f"Error registrando actividad: {str(e)}")
        return None
    
    @staticmethod
    def registrar_analitica(usuario, pagina, tiempo_duracion=None):
        """
        Registra datos analíticos solo en MongoDB
        - MongoDB: Para análisis de uso y estadísticas
        """
        try:
            analitica = AnaliticaMongo(
                usuario=usuario,
                pagina=pagina,
                tiempo_duracion=tiempo_duracion,
                fecha_creacion=datetime.now()
            )
            analitica.save()
            return analitica.id
        except Exception as e:
            print(f"Error registrando analítica: {str(e)}")
        return None
    
    @staticmethod
    def obtener_historial_chat(usuario, limite=50):
        """
        Obtiene historial de chat desde MongoDB
        """
        try:
            chats = ChatMessageMongo.objects(usuario=usuario).order_by('-fecha_creacion')[:limite]
            return list(chats)
        except Exception as e:
            print(f"Error obteniendo historial: {str(e)}")
            return []
    
    @staticmethod
    def obtener_estadisticas_usuario(usuario):
        """
        Obtiene estadísticas del usuario desde MongoDB
        """
        try:
            stats = {
                'total_chats': ChatMessageMongo.objects(usuario=usuario).count(),
                'total_notificaciones': NotificacionMongo.objects(usuario=usuario).count(),
                'total_actividad': LogActividadMongo.objects(usuario=usuario).count(),
                'total_analitica': AnaliticaMongo.objects(usuario=usuario).count()
            }
            return stats
        except Exception as e:
            print(f"Error obteniendo estadísticas: {str(e)}")
            return {}
    
    @staticmethod
    def registrar_evento_interaccion(usuario, tipo_evento, elemento, pagina, metadata=None):
        """
        Registra eventos de interacción específicos en MongoDB
        - tipo_evento: click, scroll, submit, hover, etc.
        - elemento: botón, enlace, formulario, etc.
        - pagina: URL de la página
        - metadata: datos adicionales en formato JSON
        """
        try:
            evento = EventoInteraccionMongo(
                usuario=usuario,
                tipo_evento=tipo_evento,
                elemento=elemento,
                pagina=pagina,
                metadata=metadata,
                fecha_creacion=datetime.now()
            )
            evento.save()
            return evento.id
        except Exception as e:
            print(f"Error registrando evento de interacción: {str(e)}")
        return None
    
    @staticmethod
    def registrar_click(usuario, elemento, pagina, metadata=None):
        """Registra un evento de click"""
        return DualDatabaseService.registrar_evento_interaccion(
            usuario=usuario,
            tipo_evento='click',
            elemento=elemento,
            pagina=pagina,
            metadata=metadata
        )
    
    @staticmethod
    def registrar_scroll(usuario, elemento, pagina, metadata=None):
        """Registra un evento de scroll"""
        return DualDatabaseService.registrar_evento_interaccion(
            usuario=usuario,
            tipo_evento='scroll',
            elemento=elemento,
            pagina=pagina,
            metadata=metadata
        )
    
    @staticmethod
    def registrar_submit(usuario, elemento, pagina, metadata=None):
        """Registra un evento de submit (formulario)"""
        return DualDatabaseService.registrar_evento_interaccion(
            usuario=usuario,
            tipo_evento='submit',
            elemento=elemento,
            pagina=pagina,
            metadata=metadata
        )
    
    @staticmethod
    def obtener_eventos_interaccion(usuario, limite=50):
        """
        Obtiene eventos de interacción de un usuario
        """
        try:
            eventos = EventoInteraccionMongo.objects(usuario=usuario).order_by('-fecha_creacion')[:limite]
            return list(eventos)
        except Exception as e:
            print(f"Error obteniendo eventos de interacción: {str(e)}")
            return []
