from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Redirige la raíz básica al home de usuarios
    path('', RedirectView.as_view(url='/home/', permanent=True)),
    
    # Incluye las URLs de tus aplicaciones
    path('', include('apps.users.urls')),
    path('juegos/', include('apps.juegos.urls')),

    path('traductor/', include('apps.traductor.urls')),

    path('clima/', include('apps.clima.urls')),
    path('chat/', include('apps.chat.urls')),
    path('entretenimiento/', include('apps.entretenimiento.urls')),
]