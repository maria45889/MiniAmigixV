from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Game, Score, Achievement, UserAchievement, GameSession, UserStats


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'nombre', 'descripcion', 'categoria', 'icono', 'activo', 'fecha_creacion']
        read_only_fields = ['fecha_creacion']


class ScoreSerializer(serializers.ModelSerializer):
    juego_nombre = serializers.CharField(source='juego.nombre', read_only=True)
    juego_icono = serializers.CharField(source='juego.icono', read_only=True)
    
    class Meta:
        model = Score
        fields = ['id', 'usuario', 'juego', 'juego_nombre', 'juego_icono', 'puntuacion', 
                  'nivel', 'tiempo_jugado', 'fecha']
        read_only_fields = ['fecha']


class ScoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['juego', 'puntuacion', 'nivel', 'tiempo_jugado']


class AchievementSerializer(serializers.ModelSerializer):
    desbloqueado = serializers.SerializerMethodField()
    
    class Meta:
        model = Achievement
        fields = ['id', 'nombre', 'descripcion', 'icono', 'puntos_xp', 'juego', 
                  'condicion', 'activo', 'desbloqueado']
        read_only_fields = ['condicion']
    
    def get_desbloqueado(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserAchievement.objects.filter(
                usuario=request.user,
                logro=obj
            ).exists()
        return False


class UserAchievementSerializer(serializers.ModelSerializer):
    logro_nombre = serializers.CharField(source='logro.nombre', read_only=True)
    logro_icono = serializers.CharField(source='logro.icono', read_only=True)
    logro_puntos_xp = serializers.IntegerField(source='logro.puntos_xp', read_only=True)
    
    class Meta:
        model = UserAchievement
        fields = ['id', 'usuario', 'logro', 'logro_nombre', 'logro_icono', 
                  'logro_puntos_xp', 'fecha_desbloqueo']
        read_only_fields = ['fecha_desbloqueo']


class GameSessionSerializer(serializers.ModelSerializer):
    juego_nombre = serializers.CharField(source='juego.nombre', read_only=True)
    duracion_segundos = serializers.SerializerMethodField()
    
    class Meta:
        model = GameSession
        fields = ['id', 'usuario', 'juego', 'juego_nombre', 'inicio', 'fin', 
                  'puntuacion_final', 'nivel_alcanzado', 'gano', 'duracion_segundos']
        read_only_fields = ['inicio']
    
    def get_duracion_segundos(self, obj):
        duracion = obj.duracion()
        return int(duracion) if duracion else None


class GameSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSession
        fields = ['juego', 'puntuacion_final', 'nivel_alcanzado', 'gano']


class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStats
        fields = ['id', 'usuario', 'total_puntos_xp', 'total_monedas', 'juegos_completados',
                  'racha_dias', 'ultima_jugada', 'nivel', 'insignia']
        read_only_fields = ['usuario']
