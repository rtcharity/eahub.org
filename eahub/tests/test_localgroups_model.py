from django.test import TestCase
from eahub.localgroups.models import LocalGroup, Organisership
from eahub.base.models import User


class LocalGroupTestCase(TestCase):
    def test_organisers_names(self):
        localGroup = LocalGroup()
        localGroup.save()
        user_without_profile = User()
        user_without_profile.save()
        o = Organisership(user=user_without_profile, local_group=localGroup)
        o.save()

        organisers_names = localGroup.organisers_names()

        self.assertEqual("User profile missing", organisers_names)
