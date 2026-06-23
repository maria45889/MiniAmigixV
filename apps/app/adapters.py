from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_username
from django.conf import settings
import re


class AccountAdapter(DefaultAccountAdapter):
    """
    Adaptador personalizado para allauth account
    """
    def send_mail(self, template_prefix, email, context):
        # Agregar site_url al contexto
        context['site_url'] = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
        return super().send_mail(template_prefix, email, context)

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        
        # Generar username automáticamente si no existe
        if not user.username:
            # Usar el email como base para el username
            email = user_email(user)
            if email:
                # Extraer la parte antes del @ del email
                username = email.split('@')[0]
                # Limpiar caracteres no válidos
                username = re.sub(r'[^\w.@+-]', '', username)
                # Asegurar que sea único
                base_username = username
                counter = 1
                from django.contrib.auth.models import User
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                user.username = username
            else:
                # Usar el UID de la cuenta social como fallback
                user.username = sociallogin.account.uid
        
        return user
    
    def pre_social_login(self, request, sociallogin):
        # Si el usuario ya existe, vincular la cuenta social automáticamente
        if sociallogin.user.pk:
            return
        
        # Si el email ya existe, vincular al usuario existente
        email = user_email(sociallogin.user)
        if email:
            from django.contrib.auth.models import User
            users = User.objects.filter(email=email)
            if users.exists():
                # Si hay múltiples usuarios, tomar el primero
                sociallogin.user = users.first()
