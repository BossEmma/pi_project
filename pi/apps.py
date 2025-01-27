from django.apps import AppConfig

class PiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pi'

    def ready(self):
        from .scheduler import start_scheduler
        start_scheduler()
