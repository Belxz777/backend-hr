import logging
from django.apps import AppConfig

from .log_handler import endpoint_handler 
class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    def ready(self):
        import main.signals
        logger = logging.getLogger('app')
        logger.addHandler(endpoint_handler)
        logger.setLevel(logging.INFO)