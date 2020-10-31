from django.test import TestCase

from eahub.base.models import User
from eahub.localgroups.models import LocalGroup, Organisership


class LocalGroupTestCase(TestCase):
    def test_organisers_names(self):
        local_group = LocalGroup()
        local_group.save()
        user_without_profile = User()
        user_without_profile.save()
        o = Organisership(user=user_without_profile, local_group=local_group)
        o.save()

        organisers_names = local_group.organisers_names()

        self.assertEqual("User profile missing", organisers_names)
