from django.apps import AppConfig

class PalmAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'palm_app'

    def ready(self):
        import palm_app.signals

