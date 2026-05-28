from rest_framework import serializers
from .models import Marca, Vehiculo

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ["id", "nombre"]

class VehiculoSerializer(serializers.ModelSerializer):
    marca_nombre = serializers.CharField(source="marca.nombre", read_only=True)

    class Meta:
        model = Vehiculo
        fields = ["id", "marca", "marca_nombre", "modelo", "anio", "placa", "color", "creado_en"]