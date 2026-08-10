from rest_framework import serializers
from .models import (
    UserProfile, Mision, MisionCompletada, LeccionRapida, 
    Insignia, InsigniaUsuario, Accesorio, AccesorioUsuario
)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'xp', 'nivel', 'monedas', 'racha_actual', 'racha_maxima', 'misiones_completadas', 'fecha_ultima_actividad']
        read_only_fields = ['xp', 'nivel', 'monedas', 'racha_actual', 'racha_maxima', 'misiones_completadas', 'fecha_ultima_actividad']

class MisionSerializer(serializers.ModelSerializer):
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)
    dificultad_display = serializers.CharField(source='get_dificultad_display', read_only=True)
    completada = serializers.SerializerMethodField()
    
    class Meta:
        model = Mision
        fields = ['id', 'titulo', 'descripcion', 'categoria', 'categoria_display', 'xp_recompensa', 'monedas_recompensa', 'dificultad', 'dificultad_display', 'contenido_interactivo', 'activa', 'fecha_creacion', 'completada']
        read_only_fields = ['fecha_creacion']
    
    def get_completada(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return MisionCompletada.objects.filter(usuario=request.user, mision=obj).exists()
        return False

class MisionCompletadaSerializer(serializers.ModelSerializer):
    mision_titulo = serializers.CharField(source='mision.titulo', read_only=True)
    mision_categoria = serializers.CharField(source='mision.get_categoria_display', read_only=True)
    
    class Meta:
        model = MisionCompletada
        fields = ['id', 'mision', 'mision_titulo', 'mision_categoria', 'fecha_completacion', 'xp_ganado', 'monedas_ganadas']
        read_only_fields = ['fecha_completacion', 'xp_ganado', 'monedas_ganadas']

class LeccionRapidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeccionRapida
        fields = ['id', 'titulo', 'pregunta', 'contenido', 'tiempo_estimado_minutos', 'categoria', 'xp_recompensa', 'activa', 'fecha_creacion']
        read_only_fields = ['fecha_creacion']

class InsigniaSerializer(serializers.ModelSerializer):
    obtenida = serializers.SerializerMethodField()
    
    class Meta:
        model = Insignia
        fields = ['id', 'nombre', 'descripcion', 'icono', 'xp_requerido', 'misiones_requeridas', 'condicion_especial', 'fecha_creacion', 'obtenida']
        read_only_fields = ['fecha_creacion']
    
    def get_obtenida(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return InsigniaUsuario.objects.filter(usuario=request.user, insignia=obj).exists()
        return False

class InsigniaUsuarioSerializer(serializers.ModelSerializer):
    insignia_nombre = serializers.CharField(source='insignia.nombre', read_only=True)
    insignia_icono = serializers.CharField(source='insignia.icono', read_only=True)
    insignia_descripcion = serializers.CharField(source='insignia.descripcion', read_only=True)
    
    class Meta:
        model = InsigniaUsuario
        fields = ['id', 'insignia', 'insignia_nombre', 'insignia_icono', 'insignia_descripcion', 'fecha_obtenida']
        read_only_fields = ['fecha_obtenida']

class AccesorioSerializer(serializers.ModelSerializer):
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)
    comprado = serializers.SerializerMethodField()
    
    class Meta:
        model = Accesorio
        fields = ['id', 'nombre', 'descripcion', 'icono', 'categoria', 'categoria_display', 'precio', 'xp_requerido', 'limitado', 'stock', 'fecha_creacion', 'comprado']
        read_only_fields = ['fecha_creacion']
    
    def get_comprado(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return AccesorioUsuario.objects.filter(usuario=request.user, accesorio=obj).exists()
        return False

class AccesorioUsuarioSerializer(serializers.ModelSerializer):
    accesorio_nombre = serializers.CharField(source='accesorio.nombre', read_only=True)
    accesorio_icono = serializers.CharField(source='accesorio.icono', read_only=True)
    accesorio_categoria = serializers.CharField(source='accesorio.get_categoria_display', read_only=True)
    
    class Meta:
        model = AccesorioUsuario
        fields = ['id', 'accesorio', 'accesorio_nombre', 'accesorio_icono', 'accesorio_categoria', 'fecha_compra', 'equipado']
        read_only_fields = ['fecha_compra']
