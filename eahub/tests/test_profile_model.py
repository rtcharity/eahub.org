from django.test import TestCase

from eahub.profiles.models import Profile


class ProfileTestCase(TestCase):
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
