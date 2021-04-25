from django.test import override_settings
from django.urls import reverse

from eahub.profiles.models import VisibilityEnum
from eahub.tests.cases import EAHubTestCase


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class ProfileTestCase(EAHubTestCase):
    def test_private_profile_hidden(self):
        profile = self.gen.profile(
            first_name="first", last_name="last", visibility=VisibilityEnum.PRIVATE
        )
        profile.save()
        response = self.client.get(
            reverse("profiles_app:profile", args=([profile.slug]))
        )
        self.assertEqual(response.status_code, 404)

    def test_internal_profile_hidden(self):
        profile = self.gen.profile(
            first_name="first", last_name="last", visibility=VisibilityEnum.INTERNAL
        )
        profile.save()
        response = self.client.get(
            reverse("profiles_app:profile", args=([profile.slug]))
        )
        self.assertEqual(response.status_code, 403)

    def test_internal_profile_visible_to_approved_user(self):
        profile = self.gen.profile(
            first_name="first", last_name="last", visibility=VisibilityEnum.INTERNAL
        )
        profile.save()
        profile_visitor = self.gen.profile()
        profile_visitor.is_approved = True
        self.client.force_login(profile_visitor.user)

        response = self.client.get(
            reverse("profiles_app:profile", args=([profile.slug]))
        )
        self.assertEqual(response.status_code, 200)

    def test_public_profile_visible(self):
        profile = self.gen.profile(
            first_name="first", last_name="last", visibility=VisibilityEnum.PUBLIC
        )
        profile.save()
        response = self.client.get(
            reverse("profiles_app:profile", args=([profile.slug]))
        )
        self.assertEqual(response.status_code, 200)
