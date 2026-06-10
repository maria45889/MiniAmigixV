from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')), # Include the app's URLs
    path('eventos/', include('eventos.urls')), # Include eventos URLs
    path('notificaciones/', include('notificaciones.urls')), # Include notificaciones URLs
    path('perfil/', include('perfil.urls')), # Include perfil URLs
    path('tutorial/', include('tutorial.urls')), # Include tutorial URLs
    path('sugerencias/', include('sugerencias.urls')), # Include sugerencias URLs
    path('soporte/', include('soporte.urls')), # Include soporte URLs
    path('configuracion/', include('configuracion.urls')), # Include configuracion URLs
]
