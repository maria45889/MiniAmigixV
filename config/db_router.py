# ============================================================================
# DATABASE ROUTER
# ============================================================================

class DatabaseRouter:
    """
    Controla qué modelos van a PostgreSQL (default), SQLite (sqlite) y cuáles a MongoDB (mongodb).
    """
    
    # Definimos los labels de las apps que deben usar MongoDB
    route_app_labels = {'notificaciones', 'chats', 'recomendaciones', 'analitica', 'juegos_data'}

    def db_for_read(self, model, **hints):
        """
        Determina la base de datos para operaciones de lectura.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'mongodb'
        return 'default'  # PostgreSQL por defecto

    def db_for_write(self, model, **hints):
        """
        Determina la base de datos para operaciones de escritura.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'mongodb'
        return 'default'  # PostgreSQL por defecto

    def allow_relation(self, obj1, obj2, **hints):
        """
        Permite relaciones solo si ambos modelos están en la misma base de datos.
        Nota: Django no soporta ForeignKeys reales entre PostgreSQL y MongoDB.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return obj1._meta.app_label == obj2._meta.app_label
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Asegura que las migraciones de las apps de Mongo solo ocurran en 'mongodb'.
        Las demás apps van a PostgreSQL (default).
        """
        if app_label in self.route_app_labels:
            return db == 'mongodb'
        return db == 'default'