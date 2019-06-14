import rules


@rules.predicate
def is_organiser(user, local_group):
    return local_group.organisers.filter(pk=user.pk).exists()


rules.add_perm("localgroups.change_local_group", is_organiser)
rules.add_perm("localgroups.delete_local_group", is_organiser)
