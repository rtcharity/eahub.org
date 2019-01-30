from django.apps import AppConfig


class EahubConfig(AppConfig):
    name = "eahub"

    def ready(self):
        from . import signals
