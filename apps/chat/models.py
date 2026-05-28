from django.db import models


class Marca(models.Model):
    nombre = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.nombre


class Vehiculo(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name="vehiculos")
    modelo = models.CharField(max_length=120)
    anio = models.IntegerField()
    placa = models.CharField(max_length=20, unique=True)
    color = models.CharField(max_length=60, blank=True, default="")
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.marca.nombre} {self.modelo} ({self.placa})"
