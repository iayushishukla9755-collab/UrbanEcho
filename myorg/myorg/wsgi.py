import os
from django.core.wsgi import get_wsgi_application

# Correct settings path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myorg.settings')

application = get_wsgi_application()
