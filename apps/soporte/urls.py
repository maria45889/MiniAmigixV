from django.urls import path
from . import views

urlpatterns = [
    path('', views.soporte_home, name='soporte'),
    path('tickets/', views.lista_tickets, name='lista_tickets'),
    path('crear/', views.crear_ticket, name='crear_ticket'),
    path('admin/', views.admin_tickets, name='admin_tickets'),
    path('admin/responder/<int:ticket_id>/', views.responder_ticket, name='responder_ticket'),
]
