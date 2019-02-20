from django import apps


class BaseConfig(apps.AppConfig):
    name = "eahub.base"
    verbose_name = "EA Hub"

    def ready(self):
        from . import signals
