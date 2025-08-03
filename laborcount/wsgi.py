
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'laborcount.settings')
# можно переписывать settings в разные модули
application = get_wsgi_application()
