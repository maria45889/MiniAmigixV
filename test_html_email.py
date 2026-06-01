import os
import sys
import django

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User

def test_html_email():
    print("Testing HTML email functionality...")
    
    # Get or create a test user
    user = User.objects.first()
    if not user:
        print("Creating test user...")
        user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            first_name='Test', 
            last_name='User'
        )
    
    now = timezone.localtime(timezone.now())
    autor_nombre = user.get_full_name() or user.username
    autor_email = user.email or '(sin email)'
    
    subject = "[MiniAmigixV] Nueva sugerencia: Prueba de Correo HTML"
    context = {
        'autor_nombre': autor_nombre,
        'autor_email': autor_email,
        'fecha_hora': now.strftime('%d/%m/%Y %H:%M'),
        'tipo': 'Idea',
        'tipo_clase': 'idea',
        'estado': 'Pendiente',
        'estado_clase': 'pendiente',
        'descripcion': 'Esta es una prueba para verificar que los correos ahora se envían con formato HTML bonito',
        'sugerencia_id': 999,
        'año': now.year,
    }

    # Render HTML template
    try:
        html_content = render_to_string('emails/nueva_sugerencia.html', context)
        print("HTML template rendered successfully (%d characters)" % len(html_content))
    except Exception as e:
        print("Error rendering HTML template: %s" % str(e))
        return False

    # Send email
    try:
        msg = EmailMultiAlternatives(
            subject,
            '',  # plain text version (we'll leave empty for HTML-only)
            settings.DEFAULT_FROM_EMAIL,
            ['miniamigixv@gmail.com']
        )
        msg.attach_alternative(html_content, "text/html")
        sent = msg.send()
        print("Email sent successfully, result: %d" % sent)
        return True
    except Exception as e:
        print("Error sending email: %s" % str(e))
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_html_email()
    if success:
        print("\nHTML email test completed successfully!")
        print("Check miniamigixv@gmail.com for the formatted email.")
    else:
        print("\nHTML email test failed.")