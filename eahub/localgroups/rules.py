import rules

from ..profiles.models import Profile


def is_organiser(user, local_group):
    return local_group.organisers.filter(pk=user.pk).exists()


@rules.predicate
def can_edit_group(user, local_group):
    return user.has_perm("localgroups.change_localgroup") or is_organiser(
        user, local_group
    )


@rules.predicate
def can_delete_group(user, local_group):
    return user.has_perm("localgroups.delete_localgroup") or is_organiser(
        user, local_group
    )


@rules.predicate
def is_approved(user):
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        return False
    return profile.is_approved


rules.add_perm("localgroups.create_local_group", is_approved)
rules.add_perm("localgroups.edit_group", can_edit_group)
rules.add_perm("localgroups.delete_group", can_delete_group)
