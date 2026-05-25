from django.urls import path
from .views import login_view, register_view, home_view, profile_view, update_profile, logout_view

from django.shortcuts import redirect

urlpatterns = [
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('registro/', register_view, name='registro'),
    path('register/', register_view, name='register'),
    path('home/', home_view, name='home'),
    path('perfil/', profile_view, name='perfil'),
    path('actualizar-perfil/', update_profile, name='actualizar_perfil'),
    path('logout/', logout_view, name='logout'),
    path('password-reset/', lambda request: redirect('login'), name='password_reset'),
]









