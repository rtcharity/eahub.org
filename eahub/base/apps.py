from django import apps


class BaseConfig(apps.AppConfig):
    name = "eahub.base"
    label = "eahub"
    verbose_name = "EA Hub"

    def ready(self):
        from . import signals
