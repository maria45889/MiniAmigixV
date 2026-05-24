from django.urls import path
from .views import login_view, register_view, home_view

urlpatterns = [

    path('', login_view, name='login'),

    path('registro/', register_view, name='registro'),

    path('home/', home_view, name='home'),

]

