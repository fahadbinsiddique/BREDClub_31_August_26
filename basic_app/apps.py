from django.apps import AppConfig


class BasicAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'basic_app'

    def ready(self):
        from . import signals  # noqa: F401
