import rules


@rules.predicate
def localgroup_is_public(user, local_group):
    return local_group.is_public


@rules.predicate
def is_organiser(user, local_group):
    return local_group.organisers.filter(pk=user.pk).exists()


rules.add_perm("localgroups.view_local_group", localgroup_is_public | is_organiser)
rules.add_perm("localgroups.change_local_group", is_organiser)
rules.add_perm("localgroups.delete_local_group", is_organiser)
