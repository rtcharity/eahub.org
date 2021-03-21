from django.core import exceptions


def validate_sluggable_name(name: str):
    from eahub.profiles.models import ProfileSlug, slugify_user

    if slugify_user(name) in ProfileSlug.forbidden_slugs():
        raise exceptions.ValidationError(f"The name '{name}' is not allowed")
