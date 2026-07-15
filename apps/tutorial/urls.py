from django.urls import path
from . import views

urlpatterns = [
    # Home y listas
    path('', views.tutorial_home, name='tutorial_home'),
    path('lista/', views.tutorial_list, name='tutorial_list'),
    path('categoria/<int:category_id>/', views.category_tutorials, name='category_tutorials'),
    
    # Detalles y pasos
    path('tutorial/<int:tutorial_id>/', views.tutorial_detail, name='tutorial_detail'),
    path('tutorial/<int:tutorial_id>/paso/<int:step_order>/', views.tutorial_step, name='tutorial_step'),
    
    # Acciones de usuario (requieren login)
    path('tutorial/<int:tutorial_id>/completar/<int:step_order>/', views.complete_step, name='complete_step'),
    path('tutorial/<int:tutorial_id>/calificar/', views.rate_tutorial, name='rate_tutorial'),
    path('tutorial/<int:tutorial_id>/notas/', views.save_notes, name='save_notes'),
    path('mis-tutoriales/', views.my_tutorials, name='my_tutorials'),
    
    # FAQs
    path('faq/', views.faq_list, name='faq_list'),
    path('faq/<int:faq_id>/util/', views.faq_helpful, name='faq_helpful'),
]
