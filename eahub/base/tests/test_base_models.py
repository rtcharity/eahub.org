from django.test import TestCase
from model_mommy import mommy


class UserTests(TestCase):
    def test_has_profile(self):
        user = mommy.make("base.User")

        # With no profile
        self.assertFalse(user.has_profile())

        # With a profile
        mommy.make("Profile", user=user, slug="slug")

        self.assertTrue(user.has_profile())
