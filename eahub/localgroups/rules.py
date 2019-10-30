import rules

from ..profiles.models import Profile


@rules.predicate
def is_organiser(user, local_group):
    return local_group.organisers.filter(pk=user.pk).exists()


@rules.predicate
def is_approved(user):
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        return False
    return profile.is_approved


rules.add_perm("localgroups.create_local_group", is_approved)
rules.add_perm("localgroups.change_local_group", is_organiser)
rules.add_perm("localgroups.delete_local_group", is_organiser)
