from django.contrib.auth.models import User
from rest_framework import serializers
from app.models import ConversacionChat, MensajeChat

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class MensajeChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensajeChat
        fields = ['id', 'conversacion', 'texto', 'es_usuario', 'fecha_creacion']

class ConversacionChatSerializer(serializers.ModelSerializer):
    mensajes = MensajeChatSerializer(source='mensajechat_set', many=True, read_only=True)

    class Meta:
        model = ConversacionChat
        fields = ['id', 'usuario', 'titulo', 'fecha_creacion', 'fecha_actualizacion', 'mensajes']
