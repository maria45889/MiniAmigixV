# ============================================================================
# EVENTOS URLS
# ============================================================================

from django.urls import path
from . import views

urlpatterns = [
    # List Events
    path('', views.lista_eventos, name='lista_eventos'),
    
    # Create Event
    path('crear/', views.crear_evento, name='crear_evento'),
    
    # Edit/Delete Event
    path('editar/<int:evento_id>/', views.editar_evento, name='editar_evento'),
    path('eliminar/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),
]
