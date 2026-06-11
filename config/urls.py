from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), # URLs de django-allauth
    path('', include('app.urls')), # Include the app's URLs
    path('eventos/', include('eventos.urls')), # Include eventos URLs
    path('notificaciones/', include('notificaciones.urls')), # Include notificaciones URLs
    path('perfil/', include('perfil.urls')), # Include perfil URLs
    path('tutorial/', include('tutorial.urls')), # Include tutorial URLs
    path('sugerencias/', include('sugerencias.urls')), # Include sugerencias URLs
    path('soporte/', include('soporte.urls')), # Include soporte URLs
    path('configuracion/', include('configuracion.urls')), # Include configuracion URLs
    path('estudio/', include('estudio.urls')), # Include estudio URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
