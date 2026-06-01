import os
import sys
import django

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.core import mail

def test_web_suggestion_flow():
    print("Testing web suggestion flow with HTML email...")
    
    # Create a test user and log in
    user = User.objects.first()
    if not user:
        user = User.objects.create_user(
            username='webtest',
            email='webtest@example.com',
            first_name='Web',
            last_name='Test',
            password='testpass123'
        )
    
    # Create test client and login
    client = Client()
    login_success = client.login(username=user.username, password='testpass123')
    if not login_success:
        print("Failed to login test user")
        return False
    
    # Clear any existing emails
    mail.outbox = []
    
    # Prepare suggestion data
    suggestion_data = {
        'titulo': 'Prueba de flujo web completo',
        'descripcion': 'Esta sugerencia viene de una prueba del flujo web completo para verificar que los correos HTML se envian correctamente al enviar una sugerencia desde la interfaz.',
        'tipo': 'mejora'
    }
    
    # Make POST request to crear_sugerencia
    response = client.post('/sugerencias/crear/', data=suggestion_data)
    
    print("Response status code:", response.status_code)
    print("Response content:", response.content.decode()[:200]+"...")
    
    # Check if any emails were sent
    print("Number of emails sent:", len(mail.outbox))
    
    if len(mail.outbox) > 0:
        email = mail.outbox[0]
        print("Email subject:", email.subject)
        print("Email to:", email.to)
        print("Email from:", email.from_email)
        print("Email alternatives count:", len(email.alternatives))
        
        # Check if we have HTML alternative
        html_present = False
        for alt, mimetype in email.alternatives:
            if mimetype == 'text/html':
                html_present = True
                print("HTML part length:", len(alt), "characters")
                # Print a snippet of HTML
                print("HTML snippet:", alt[:300]+"...")
                break
        
        if html_present:
            print("SUCCESS: HTML email was sent successfully!")
            return True
        else:
            print("ERROR: No HTML alternative found in email")
            return False
    else:
        print("ERROR: No emails were sent")
        return False

if __name__ == "__main__":
    success = test_web_suggestion_flow()
    if success:
        print("\nWeb flow test completed successfully!")
        print("Check the email backend output (console) or actual email if SMTP configured.")
    else:
        print("\nWeb flow test failed.")