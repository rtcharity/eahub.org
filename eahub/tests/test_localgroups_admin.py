from django.test import TestCase

from eahub.base.models import User
from eahub.localgroups.admin import LocalGroupResource
from eahub.localgroups.models import LocalGroup, Organisership
from eahub.profiles.models import Profile


class LocalGroupAdminTestCase(TestCase):
    def setUp(self):
        local_group = LocalGroup()
        local_group.id = 1
        local_group.save()
        self.local_group = local_group

        user1 = User()
        user1.email = "1@email.com"
        user1.save()
        self.user_peter_1 = user1

        user2 = User()
        user2.email = "2@email.com"
        user2.save()

        user3 = User()
        user3.email = "3@email.com"
        user3.save()

        profile1 = Profile()
        name1 = "Peter"
        profile1.name = name1
        profile1.user = user1
        profile1.save()

        profile2 = Profile()
        name2 = "Mary"
        profile2.name = name2
        profile2.user = user2
        profile2.save()

        profile3 = Profile()
        name3 = "Peter"
        profile3.name = name3
        profile3.user = user3
        profile3.save()

        self.user_peter_2 = user3

        o1 = Organisership(user=user1, local_group=local_group)
        o1.save()

        o2 = Organisership(user=user2, local_group=local_group)
        o2.save()

    def test_hydrate_organiser_where_users_with_same_name_and_one_already_organiser(
        self
    ):
        local_group_resource = LocalGroupResource()
        row = {"id": "1"}
        user = local_group_resource.hydrate_organiser("Peter", row)

        self.assertEqual(self.user_peter_1, user)

    def test_hydrate_organiser_where_users_with_same_name_and_already_organisers(self):
        o = Organisership(user=self.user_peter_2, local_group=self.local_group)
        o.save()

        local_group_resource = LocalGroupResource()
        row = {"id": "1"}
        user = local_group_resource.hydrate_organiser("Peter", row)

        self.assertEqual(self.user_peter_2, user)
        