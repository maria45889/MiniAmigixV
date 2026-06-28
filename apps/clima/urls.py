from django.urls import path
from .views import clima_view, obtener_clima, geolocalizar

urlpatterns = [
    path('', clima_view, name='clima'),
    path('api/obtener-clima/', obtener_clima, name='obtener_clima'),
    path('api/geolocalizar/', geolocalizar, name='geolocalizar'),
]
