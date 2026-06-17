class DatabaseRouter:
    """
    Controla qué modelos van a SQLite (default) y cuáles a MongoDB (mongodb).
    """
    
    # Definimos los labels de las apps que deben usar MongoDB
    route_app_labels = {'notificaciones', 'chats', 'recomendaciones', 'analitica', 'juegos_data'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'mongodb'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'mongodb'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Permite relaciones solo si ambos modelos están en la misma base de datos.
        Nota: Django no soporta ForeignKeys reales entre SQLite y MongoDB.
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
        """
        if app_label in self.route_app_labels:
            return db == 'mongodb'
        return db == 'default'