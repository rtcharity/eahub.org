from django.test import TestCase, override_settings
from faker import Faker
from model_bakery import baker

from eahub.base.models import User
from eahub.localgroups.models import LocalGroup
from eahub.profiles.models import Profile


class Gen:
    def __init__(self):
        self.faker = Faker()

    def group(self, **kwargs) -> LocalGroup:
        return baker.make("localgroups.LocalGroup", slug="", **kwargs)

    def profile(self, **kwargs) -> Profile:
        return baker.make("profiles.Profile", slug="", **kwargs)

    def user(self, **kwargs) -> User:
        return baker.make("base.User", **kwargs)

    def email(self) -> str:
        return self.faker.unique.email()


@override_settings(IS_ENABLE_ALGOLA=False)
class EAHubTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gen = Gen()
        super().setUpClass()
