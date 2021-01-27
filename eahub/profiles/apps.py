from django import apps


class ProfilesConfig(apps.AppConfig):
    name = "eahub.profiles"
    verbose_name = "Profiles"

    # noinspection PyUnresolvedReferences
    def ready(self):
        from eahub.profiles.receivers import clear_the_cache  # noqa: F401
        from eahub.profiles.receivers import on_profile_change  # noqa: F401
        from eahub.profiles.receivers import on_profile_creation  # noqa: F401
