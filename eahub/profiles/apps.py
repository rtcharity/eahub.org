from django import apps


class ProfilesConfig(apps.AppConfig):
    name = "eahub.profiles"
    verbose_name = "Profiles"

    def ready(self):
        import eahub.profiles.receivers  # noqa: F401
