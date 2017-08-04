"""
WSGI config for Natalia project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
from engine import taskcontrol

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Natalia.settings")

application = get_wsgi_application()

taskcontrol.scheduleinit()
