from asgiref.wsgi import WsgiToAsgi
from django.core.wsgi import get_wsgi_application

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "asa_project.settings")

application = WsgiToAsgi(get_wsgi_application()) 