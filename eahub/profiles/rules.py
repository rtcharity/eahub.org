import rules

from .models import Profile


@rules.predicate
def profile_is_generally_visible(user, profile):
    return profile.is_public and profile.is_approved


@rules.predicate
def is_profile_of_user(user, profile):
    return user == profile.user


@rules.predicate
def is_approved(user):
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        return False
    return profile.is_approved


rules.add_perm(
    "profiles.view_profile", profile_is_generally_visible | is_profile_of_user
)
rules.add_perm("profiles.message_users", is_approved)
