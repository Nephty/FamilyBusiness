import sys

from django.apps import AppConfig


class WalletConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wallet'

    def ready(self):
        if 'runserver' in sys.argv or 'shell_plus' in sys.argv:
            from . import scheduler
            scheduler.start()