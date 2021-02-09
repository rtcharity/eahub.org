import random

from eahub.base.models import User
from eahub.localgroups.models import LocalGroup, Organisership
from eahub.profiles.models import CauseArea, Profile, ProfileAnalyticsLog
from eahub.tests.cases import EAHubTestCase


class ProfileTestCase(EAHubTestCase):
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
            "offering",
            "looking_for",
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
        analytics_logs_slug = ProfileAnalyticsLog.objects.filter(
            profile=profile, field="slug"
        )
        analytics_logs_id = ProfileAnalyticsLog.objects.filter(
            profile=profile, field="id"
        )
        analytics_logs_user_id = ProfileAnalyticsLog.objects.filter(
            profile=profile, field="user"
        )
        analytics_logs_email_visible = ProfileAnalyticsLog.objects.filter(
            profile=profile, field="email_visible"
        )

        self.assertEqual("User1", analytics_logs_name.first().new_value)
        self.assertEqual("False", analytics_logs_is_approved.first().new_value)
        self.assertEqual("True", analytics_logs_is_public.first().new_value)
        self.assertEqual("user1", analytics_logs_slug.first().new_value)
        self.assertEqual(str(profile.id), analytics_logs_id.first().new_value)
        self.assertEqual(str(profile.user), analytics_logs_user_id.first().new_value)
        self.assertEqual("False", analytics_logs_email_visible.first().new_value)
        self.assertEqual(8, len(analytics_logs))
        self.assertTrue(all(x.action == "Create" for x in analytics_logs))
        self.assertTrue(
            all(
                x.action_uuid == analytics_logs.first().action_uuid
                for x in analytics_logs
            )
        )
        self.assertTrue(
            all(x.time == analytics_logs.first().time for x in analytics_logs)
        )

    def test_save_profile_analytics_on_user_change(self):
        profile = self.gen.profile()
        profile.user.password = "new"
        profile.user.save()
        ProfileAnalyticsLog.objects.get(profile=profile, field="password")

    def test_skip_profile_analytics_creation_on_change_without_profile(self):
        user = self.gen.user()
        self.assertEqual(ProfileAnalyticsLog.objects.all().count(), 0)

        user.password = "new"
        user.save()
        self.assertEqual(ProfileAnalyticsLog.objects.all().count(), 0)

    def test_save_profile_analytics_creation_on_change_email(self):
        profile = self.gen.profile()
        profile.user.email = self.gen.email()
        profile.user.save()
        ProfileAnalyticsLog.objects.get(
            profile=profile,
            new_value=profile.user.email,
        )

    def test_save_profile_analytics_on_change(self):
        profile = create_profile("test@email.com", "User1")

        profile.name = "User1New"
        profile.cause_areas = [CauseArea.BUILDING_EA_COMMUNITIES]
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

        self.assertEqual("User1New", analytics_logs_name_updated.first().new_value)
        self.assertEqual(
            str(["Building EA communities"]),
            analytics_logs_cause_area_updated.first().new_value,
        )
        self.assertEqual(2, len(analytics_logs_update))
        self.assertTrue(
            all(
                x.action_uuid == analytics_logs_update.first().action_uuid
                for x in analytics_logs_update
            )
        )
        self.assertTrue(
            all(
                x.time == analytics_logs_update.first().time
                for x in analytics_logs_update
            )
        )

    def test_has_community_details_returns_false_if_none(self):
        profile = create_profile("test@email.com", "peter")

        self.assertFalse(profile.has_community_details())

    def test_has_community_details_returns_true_if_free_text_field_set(self):
        profile = create_profile("test@email.com", "peter")

        field_names = ["topics_i_speak_about", "offering", "looking_for"]
        setattr(profile, random.choice(field_names), "something")

        self.assertTrue(profile.has_community_details())


def create_profile(email, username):
    user = User.objects.create(email=email)
    profile = Profile.objects.create(user=user, name=username)

    return profile
