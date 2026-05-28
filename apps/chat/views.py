from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny

from .models import Marca, Vehiculo
from .permissions import IsAdminOrReadOnly
from .serializers import MarcaSerializer, VehiculoSerializer


def chat_view(request):
    return render(request, "chat/index.html")


class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all().order_by("id")
    serializer_class = MarcaSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["nombre"]
    ordering_fields = ["id", "nombre"]


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.select_related("marca").all().order_by("-id")
    serializer_class = VehiculoSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["marca"]
    search_fields = ["modelo", "placa", "color", "marca__nombre"]
    ordering_fields = ["id", "anio", "modelo", "placa", "creado_en"]

    def get_queryset(self):
        queryset = super().get_queryset()
        anio_min = self.request.query_params.get("anio_min")
        anio_max = self.request.query_params.get("anio_max")

        if anio_min:
            queryset = queryset.filter(anio__gte=int(anio_min))
        if anio_max:
            queryset = queryset.filter(anio__lte=int(anio_max))

        return queryset

    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()]
        return super().get_permissions()
