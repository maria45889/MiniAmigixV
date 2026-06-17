import os, sys, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
import django
django.setup()
try:
    from allauth.socialaccount.models import SocialAccount
    qs = SocialAccount.objects.order_by('-id')[:20]
    for s in qs:
        print(s.id, s.provider, s.uid, getattr(s.user, 'id', None), getattr(s.user, 'username', None))
except Exception as e:
    print('No socialaccount or error:', e)
