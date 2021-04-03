from rest_framework.test import APITestCase

from eahub.profiles.models import ProfileTagTypeEnum
from eahub.tests.cases import EAHubTestCase


class TagsApiTestCase(EAHubTestCase, APITestCase):
    def test_tags_count(self):
        tag1 = self.gen.tag(
            types=[ProfileTagTypeEnum.GENERIC, ProfileTagTypeEnum.EXPERTISE_AREA]
        )
        tag2 = self.gen.tag(types=[ProfileTagTypeEnum.EXPERTISE_AREA])
        tag3 = self.gen.tag(types=[ProfileTagTypeEnum.CAUSE_AREA])
        profile1 = self.gen.profile()
        profile2 = self.gen.profile()
        profile3 = self.gen.profile()
        profile1.tags_cause_area.add(tag3)
        profile2.tags_generic.add(tag1)
        profile3.tags_expertise_area.add(tag1, tag2)
        self.assertEqual(tag1.count(), 2)
        self.assertEqual(tag2.count(), 1)
        self.assertEqual(tag3.count(), 1)
