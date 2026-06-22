import os
import django

# Setup Django first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Now import models and test utilities
from django.test import RequestFactory
from django.contrib.auth.models import User
from app.views import download_media_api

# Create a request factory
factory = RequestFactory()
request = factory.get('/api/download-media/', {'url': 'https://www.youtube.com/watch?v=tav0XtpFN4A&list=RDMMtav0XtpFN4A&start_radio=1', 'format': 'mp3'})

# Get or create a dummy user
user = User.objects.filter(is_superuser=True).first()
if not user:
    user, _ = User.objects.get_or_create(username='testadmin', email='test@example.com')
request.user = user

print("Invoking download_media_api view...")
try:
    response = download_media_api(request)
    print("Response status:", response.status_code)
    if response.status_code == 200:
        print("Success! FileResponse returned.")
        print("Headers:", dict(response.items()))
    else:
        print("Error content:", response.content.decode('utf-8', errors='ignore'))
except Exception as e:
    import traceback
    traceback.print_exc()
