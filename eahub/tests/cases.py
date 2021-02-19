from typing import List

from django.test import TestCase, override_settings
from faker import Faker
from model_bakery import baker

from eahub.base.models import User
from eahub.localgroups.models import LocalGroup
from eahub.profiles.models import (
    Profile,
    ProfileTag,
    ProfileTagType,
    ProfileTagTypeEnum,
)


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

    def tag(self, types: List[ProfileTagTypeEnum] = [], **kwargs) -> ProfileTag:
        type_instances = []
        for tag_type in types:
            type_instance = ProfileTagType.objects.get_or_create(type=tag_type)[0]
            type_instances.append(type_instance)
        tag = baker.make("profiles.ProfileTag", **kwargs)
        tag.types.set(type_instances)
        return tag


@override_settings(IS_ENABLE_ALGOLA=False)
class EAHubTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gen = Gen()
        super().setUpClass()
