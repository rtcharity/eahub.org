import rules


@rules.predicate
def profile_is_public(user, profile):
    return profile.is_public


@rules.predicate
def is_profile_of_user(user, profile):
    return user == profile.user


rules.add_perm("profiles.view_profile", profile_is_public | is_profile_of_user)
