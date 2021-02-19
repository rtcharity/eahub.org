from rest_framework.test import APITestCase

from eahub.profiles.models import Profile
from eahub.profiles.models import ProfileTagTypeEnum
from eahub.tests.cases import EAHubTestCase


class TagsApiTestCase(EAHubTestCase, APITestCase):
    def test_tags_creation(self):
        profile = self.gen.profile()
        tag = self.gen.tag(types=[ProfileTagTypeEnum.GENERIC])
        response = self.client.put(
            self._url_detail(profile.pk),
            {"tags_pks": [tag.pk]},
        )
        self.assertEqual(response.data["tags_pks"], [tag.pk])

    def test_tags_retrieval(self):
        profile = self.gen.profile()
        tag1 = self.gen.tag(types=[ProfileTagTypeEnum.GENERIC])
        tag2 = self.gen.tag(types=[ProfileTagTypeEnum.GENERIC])
        profile.tags.add(tag1, tag2)

        response = self.client.get(self._url_detail(profile.pk))
        self.assertEqual(response.data["tags_pks"], [tag1.pk, tag2.pk])
        self.assertEqual(response.data["tags"][0]["name"], tag1.name)
        self.assertEqual(
            response.data["tags"][0]["types"][0]["type"],
            ProfileTagTypeEnum.GENERIC.value
        )

    def test_cause_areas_deletion(self):
        profile = self.gen.profile()
        tag1 = self.gen.tag(types=[ProfileTagTypeEnum.CAUSE_AREA])
        tag2 = self.gen.tag(types=[ProfileTagTypeEnum.CAUSE_AREA])
        profile.tags.add(tag1, tag2)

        self.client.patch(
            self._url_detail(profile.pk),
            data={"cause_areas_new_pks": [tag1.pk]}
        )
        profile_updated = Profile.objects.get(pk=profile.pk)
        self.assertTrue(profile_updated.cause_areas_new.filter(pk=tag1.pk).exists())
        self.assertFalse(profile_updated.cause_areas_new.filter(pk=tag2.pk).exists())

    def _url_detail(self, profile_pk: int) -> str:
        return f"/profile/api/profiles/{profile_pk}/"
