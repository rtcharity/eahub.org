from django.test import TestCase, override_settings

from eahub.base.models import User
from eahub.localgroups.models import LocalGroup, Organisership
from eahub.profiles.models import CauseArea, Profile, ProfileAnalyticsLog


@override_settings(IS_ENABLE_ALGOLA=False)
class ProfileTestCase(TestCase):
    def test_get_is_organiser(self):
        profile = create_profile("test@email.com", "User1")

        local_group = LocalGroup()
        local_group.save()

        o = Organisership(user=profile.user, local_group=local_group)
        o.save()

        self.assertTrue(profile.get_is_organiser())

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

    def test_save_analytics_on_profile_creation(self):
        profile = create_profile("test@email.com", "User1")

        analytics_logs = ProfileAnalyticsLog.objects.filter(profile=profile)

        analytics_logs_name = ProfileAnalyticsLog.objects.filter(
            profile=profile, field="name"
        )
        analytics_logs_is_approved = ProfileAnalyticsLog.objects.filter(
            profile=profile, field="is_approved"
        )
        analytics_logs_is_public = ProfileAnalyticsLog.objects.filter(
            profile=profile, field="is_public"
        )
        analytics_logs_slug_changed = ProfileAnalyticsLog.objects.filter(
            profile=profile, field="slug_changed"
        )
        analytics_logs_slug = ProfileAnalyticsLog.objects.filter(
            profile=profile, field="slug"
        )
        analytics_logs_id = ProfileAnalyticsLog.objects.filter(
            profile=profile, field="id"
        )
        analytics_logs_user_id = ProfileAnalyticsLog.objects.filter(
            profile=profile, field="user_id"
        )
        analytics_logs_email_visible = ProfileAnalyticsLog.objects.filter(
            profile=profile, field="email_visible"
        )

        self.assertEqual("User1", analytics_logs_name[0].value)
        self.assertEqual("False", analytics_logs_is_approved[0].value)
        self.assertEqual("True", analytics_logs_is_public[0].value)
        self.assertEqual("False", analytics_logs_slug_changed[0].value)
        self.assertEqual("user1", analytics_logs_slug[0].value)
        self.assertEqual(str(profile.id), analytics_logs_id[0].value)
        self.assertEqual(str(profile.user.id), analytics_logs_user_id[0].value)
        self.assertEqual("False", analytics_logs_email_visible[0].value)
        self.assertEqual(8, len(analytics_logs))
        self.assertTrue(all(x.action == "Create" for x in analytics_logs))
        self.assertTrue(
            all(x.action_uuid == analytics_logs[0].action_uuid for x in analytics_logs)
        )

    def test_save_analytics_on_change(self):
        profile = create_profile("test@email.com", "User1")

        profile.name = "User1New"
        profile.cause_areas = [CauseArea.META]
        profile.save()

        analytics_logs_name_updated = ProfileAnalyticsLog.objects.filter(
            profile=profile, field="name", action="Update"
        )

        analytics_logs_cause_area_updated = ProfileAnalyticsLog.objects.filter(
            profile=profile, field="cause_areas", action="Update"
        )

        analytics_logs_update = ProfileAnalyticsLog.objects.filter(
            profile=profile, action="Update"
        )

        self.assertEqual("User1New", analytics_logs_name_updated[0].value)
        self.assertEqual(
            str([CauseArea.META]), analytics_logs_cause_area_updated[0].value
        )
        self.assertEqual(2, len(analytics_logs_update))
        self.assertTrue(
            all(
                x.action_uuid == analytics_logs_update[0].action_uuid
                for x in analytics_logs_update
            )
        )


def create_profile(email, username):
    user = User()
    user.email = email
    user.save()

    profile = Profile()
    profile.user = user
    profile.name = username
    profile.save()

    return profile
