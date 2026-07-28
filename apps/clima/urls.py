# ============================================================================
# CLIMA URLS
# ============================================================================

from django.urls import path
from .views import clima_view, geolocalizar, obtener_clima

urlpatterns = [
    # Main View
    path('', clima_view, name='clima'),
    
    # API Endpoints
    path('api/obtener-clima/', obtener_clima, name='obtener_clima'),
    path('api/geolocalizar/', geolocalizar, name='geolocalizar'),
]
