from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('apps.users.urls')),

    # 🔐 AUTH DJANGO (IMPORTANTE)
    path('accounts/', include('django.contrib.auth.urls')),
]