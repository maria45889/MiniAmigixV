from rest_framework import serializers

class ServiceTypeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)
    description = serializers.CharField(required=False, allow_blank=True)
    base_price = serializers.FloatField(required=False)
    is_active = serializers.BooleanField(default=True)

class VehicleServiceSerializer(serializers.Serializer):
    vehiculo_id = serializers.IntegerField()        # ID of Vehiculo (Postgres)
    service_type_id = serializers.CharField()       # ObjectId (string) of service_types
    date = serializers.DateField(required=False)    # Example: 2026-02-04
    kilometers = serializers.IntegerField(required=False)
    cost = serializers.FloatField(required=False)
    notes = serializers.CharField(required=False, allow_blank=True)