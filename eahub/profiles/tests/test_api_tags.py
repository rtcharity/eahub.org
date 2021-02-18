from rest_framework.test import APITestCase

from eahub.tests.cases import EAHubTestCase


class TagsApiTestCase(EAHubTestCase, APITestCase):
    def test_tags_creation(self):
        profile = self.gen.profile()
        tag = self.gen.tag()
        response = self.client.put(
            self._url_detail(profile.pk),
            {"tags_pks": [tag.pk]},
        )
        self.assertEqual(response.data["tags_pks"], [tag.pk])

    def test_tags_retrieval_pks(self):
        profile = self.gen.profile()
        tag1 = self.gen.tag()
        tag2 = self.gen.tag()
        profile.tags.add(tag1, tag2)

        response = self.client.get(self._url_detail(profile.pk))
        self.assertEqual(response.data["tags_pks"], [tag1.pk, tag2.pk])
        self.assertEqual(response.data["tags"][0]["name"], tag1.name)

    def _url_detail(self, profile_pk: int) -> str:
        return f"/profile/api/profiles/{profile_pk}/"
