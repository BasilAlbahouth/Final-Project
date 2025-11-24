"""
ASGI config for palm_diagnosis project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'palm_diagnosis.settings')

application = get_asgi_application()

