# ============================================================================
# ESTUDIO URLS
# ============================================================================

from django.urls import path
from . import views

urlpatterns = [
    # Main View
    path('', views.estudio, name='estudio'),
    
    # Notes
    path('api/guardar-nota/', views.guardar_nota, name='guardar_nota'),
    path('api/eliminar-nota/<uuid:nota_id>/', views.eliminar_nota, name='eliminar_nota'),
    path('api/obtener-notas/', views.obtener_notas, name='obtener_notas'),
    
    # Summaries
    path('api/resumir-texto/', views.resumir_texto, name='resumir_texto'),
    path('api/obtener-resumenes/', views.obtener_resumenes, name='obtener_resumenes'),
    path('api/eliminar-resumen/<uuid:resumen_id>/', views.eliminar_resumen, name='eliminar_resumen'),
    
    # Statistics & Sessions
    path('api/obtener-estadisticas/', views.obtener_estadisticas, name='obtener_estadisticas'),
    path('api/guardar-sesion-estudio/', views.guardar_sesion_estudio, name='guardar_sesion_estudio'),
    path('api/guardar-pomodoro/', views.guardar_pomodoro, name='guardar_pomodoro'),
]
