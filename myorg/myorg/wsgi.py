"""
WSGI config for myorg project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.urls import path, include

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myorg.myorg.settings')

application = get_wsgi_application()



urlpatterns = [
    path('', include('public_issue.urls')),
]
