"""
WSGI config for reactnative-backend project.

"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reactnative.settings.dev")

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
