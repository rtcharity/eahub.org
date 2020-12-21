from django.test import TestCase

from eahub.base.models import User
from eahub.localgroups.models import LocalGroup, Organisership
from eahub.profiles.models import Profile


class ProfileTestCase(TestCase):
    def test_is_organiser(self):
        user = User()
        user.email = "test00@email.com"
        user.save()

        profile = Profile()
        profile.user = user
        profile.save()

        local_group = LocalGroup()
        local_group.save()

        o = Organisership(user=user, local_group=local_group)
        o.save()

        self.assertTrue(profile.is_organiser())

    def test_get_exportable_field_names(self):
        actual = Profile.get_exportable_field_names()

        expected_field_names = [
            "id",
            "user",
            "slug",
            "is_public",
            "is_approved",
            "name",
            "image",
            "city_or_town",
            "country",
            "linkedin_url",
            "facebook_url",
            "personal_website_url",
            "lat",
            "lon",
            "cause_areas",
            "available_to_volunteer",
            "open_to_job_offers",
            "expertise_areas",
            "career_interest_areas",
            "available_as_speaker",
            "email_visible",
            "topics_i_speak_about",
            "organisational_affiliations",
            "summary",
            "giving_pledges",
            "legacy_record",
            "local_groups",
        ]

        self.assertListEqual(expected_field_names, actual)
