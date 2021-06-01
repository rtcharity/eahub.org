from typing import Tuple

from rest_framework.test import APITestCase

from eahub.profiles.models import Profile, ProfileTag, ProfileTagTypeEnum
from eahub.tests.cases import EAHubTestCase


class TagsApiTestCase(EAHubTestCase, APITestCase):
    def test_creation(self):
        profile, _, _, _ = self._generate_tags()
        self.client.force_login(profile.user)
        response = self.client.post(
            f"/profile/api/profiles/tags/create/",
            data={
                "name": "Management",
                "type": ProfileTagTypeEnum.CAREER_INTEREST.value,
            },
            format="json",
        )
        tag = ProfileTag.objects.get(pk=response.data["pk"])
        self.assertEqual(tag.author, profile)

    def test_addition(self):
        # noinspection PyTypeChecker
        for tag_type in ProfileTagTypeEnum:
            self._test_addition(tag_type)

    def test_retrieval(self):
        # noinspection PyTypeChecker
        for tag_type in ProfileTagTypeEnum:
            self._test_retrieval(tag_type)

    def test_deletion(self):
        # noinspection PyTypeChecker
        for tag_type in ProfileTagTypeEnum:
            self._test_deletion(tag_type)

    def _test_addition(self, type_enum: ProfileTagTypeEnum):
        profile, tag1, tag2, tags_field_name = self._generate_tags(type_enum)
        tag3 = self.gen.tag(types=[type_enum])
        response = self.client.patch(
            self._url_detail(profile.pk),
            data={f"{tags_field_name}_pks": [tag1.pk, tag2.pk, tag3.pk]},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(tag1.pk, response.data[f"{tags_field_name}_pks"])
        self.assertIn(tag2.pk, response.data[f"{tags_field_name}_pks"])
        self.assertIn(tag3.pk, response.data[f"{tags_field_name}_pks"])

    def _test_retrieval(self, type_enum: ProfileTagTypeEnum):
        profile, tag1, tag2, tags_field_name = self._generate_tags(type_enum)
        response = self.client.get(self._url_detail(profile.pk))
        self.assertEqual(response.status_code, 200)
        tags = response.data[tags_field_name]
        self.assertIn(tag1.pk, response.data[f"{tags_field_name}_pks"])
        self.assertIn(tag2.pk, response.data[f"{tags_field_name}_pks"])
        for tag in tags:
            if tag["name"] == tag1.name:
                self.assertEqual(tag["types"][0]["type"], type_enum.value)

    def _test_deletion(self, type_enum: ProfileTagTypeEnum):
        profile, tag1, tag2, tags_field_name = self._generate_tags(type_enum)
        response = self.client.patch(
            self._url_detail(profile.pk),
            data={f"{tags_field_name}_pks": [tag1.pk]},
        )
        self.assertEqual(response.status_code, 200)
        profile_updated = Profile.objects.get(pk=profile.pk)
        tags_field = getattr(profile_updated, tags_field_name)
        self.assertTrue(tags_field.filter(pk=tag1.pk).exists())
        self.assertFalse(tags_field.filter(pk=tag2.pk).exists())

    def _generate_tags(
        self,
        type_enum: ProfileTagTypeEnum = ProfileTagTypeEnum.GENERIC,
    ) -> Tuple[Profile, ProfileTag, ProfileTag, str]:
        profile = self.gen.profile()
        tag1 = self.gen.tag(types=[type_enum])
        tag2 = self.gen.tag(types=[type_enum])
        tags_field_name = f"tags_{type_enum.value}"
        tags_field = getattr(profile, tags_field_name)
        tags_field.set([tag1, tag2])
        return profile, tag1, tag2, tags_field_name

    def _url_detail(self, profile_pk: int) -> str:
        return f"/profile/api/profiles/{profile_pk}/"
