from django.urls import path
from .views import traductor_view, traducir_texto, detectar_idioma, obtener_idiomas_soportados, traducir_imagen, traducir_documento

urlpatterns = [
    path('', traductor_view, name='traductor'),
    path('api/traducir/', traducir_texto, name='traducir_texto'),
    path('api/detectar-idioma/', detectar_idioma, name='detectar_idioma'),
    path('api/idiomas-soportados/', obtener_idiomas_soportados, name='idiomas_soportados'),
    path('api/traducir-imagen/', traducir_imagen, name='traducir_imagen'),
    path('api/traducir-documento/', traducir_documento, name='traducir_documento'),
]
