import os
import sys
from django.core.wsgi import get_wsgi_application

# assuming your Django settings file is at '/home/myusername/mysite/mysite/settings.py'
path = '/home/HyTacker20/devchallenge_excel'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'


application = get_wsgi_application()
