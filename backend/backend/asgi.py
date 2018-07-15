import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = "backend.settings"
django.setup()

from channels.routing import get_default_application

application = get_default_application()
