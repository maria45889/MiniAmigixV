from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import RegisterView, UserProfileView, ChatHistoryView, ChatSendView, UpdateLanguageView, CustomTokenObtainPairView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('chat/history/', ChatHistoryView.as_view(), name='chat_history'),
    path('chat/send/', ChatSendView.as_view(), name='chat_send'),
    path('update-language/', UpdateLanguageView.as_view(), name='update_language'),
]
