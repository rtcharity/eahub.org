import rules

from .models import Profile, VisibilityEnum


@rules.predicate
def profile_is_visible(user, profile):
    return (profile.visibility == VisibilityEnum.PUBLIC or (profile.visibility == VisibilityEnum.INTERNAL and is_approved(user) )) and profile.is_approved


@rules.predicate
def is_profile_of_user(user, profile):
    return user == profile.user


@rules.predicate
def is_approved(user):
    try:
        profile = user.profile
    except (Profile.DoesNotExist, AttributeError):
        return False
    return profile.is_approved


rules.add_perm(
    "profiles.view_profile", profile_is_visible | is_profile_of_user
)
rules.add_perm("profiles.message_users", is_approved)
