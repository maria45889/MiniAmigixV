#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from django.template.loader import render_to_string

print("=" * 60)
print("TEST DE CONFIGURACIÓN DE EMAIL")
print("=" * 60)

print(f"\nEMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NO CONFIGURADA'}")

print("\n" + "=" * 60)
print("ENVIANDO EMAIL DE PRUEBA...")
print("=" * 60)

try:
    # Email simple de prueba
    subject = "🧪 Test de Email - MiniAmigixV"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [settings.EMAIL_HOST_USER]  # Enviar al mismo remitente para probar
    
    # Renderizar HTML de prueba
    html_content = render_to_string('emails/evento_creado.html', {
        'username': 'Usuario de Prueba',
        'titulo': 'Evento de Prueba',
        'fecha': '11/05/2027 01:01',
        'descripcion': 'Este es un email de prueba para verificar la configuración SMTP.',
        'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000')
    })
    
    # Crear email con HTML
    email = EmailMultiAlternatives(subject, '', from_email, to_email)
    email.attach_alternative(html_content, 'text/html')
    
    result = email.send(fail_silently=False)
    
    print("\n✅ EMAIL ENVIADO EXITOSAMENTE!")
    print(f"Resultado: {result}")
    print(f"Destinatario: {to_email[0]}")
    print("\nPor favor revisa tu bandeja de entrada y spam en Gmail.")
    
except Exception as e:
    print("\n❌ ERROR AL ENVIAR EMAIL:")
    print(f"Tipo de error: {type(e).__name__}")
    print(f"Mensaje: {str(e)}")
    print("\n" + "=" * 60)
    print("POSIBLES SOLUCIONES:")
    print("=" * 60)
    print("1. Verifica que la contraseña de aplicación de Gmail sea correcta")
    print("2. Habilita la verificación en 2 pasos en tu cuenta de Google")
    print("3. Genera una nueva contraseña de aplicación en:")
    print("   https://myaccount.google.com/apppasswords")
    print("4. Asegúrate de usar 'Correo' como la aplicación")
    print("5. Actualiza EMAIL_HOST_PASSWORD en settings.py con la nueva contraseña")
    print("=" * 60)
