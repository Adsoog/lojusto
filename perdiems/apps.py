from django.apps import AppConfig

class PerdiemsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'perdiems'

    def ready(self):
        import perdiems.signals 