from django.urls import path
from . import views

urlpatterns = [
    path('', views.soporte_home, name='soporte'),
    path('tickets/', views.lista_tickets, name='lista_tickets'),
    path('crear/', views.crear_ticket, name='crear_ticket'),
]
