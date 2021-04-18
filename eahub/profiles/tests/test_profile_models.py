from typing import List

from eahub.localgroups.models import LocalGroup, Organisership
from eahub.profiles.legacy import CauseArea
from eahub.profiles.models import ProfileAnalyticsLog
from eahub.tests.cases import EAHubTestCase


class ProfileTestCase(EAHubTestCase):
    def test_is_organiser(self):
        profile = self.gen.profile()
        local_group = LocalGroup.objects.create()
        o = Organisership(user=profile.user, local_group=local_group)
        o.save()
        self.assertTrue(profile.is_organiser())

    def test_save_analytics_on_profile_creation(self):
        first_name = "User1"
        profile = self.gen.profile(first_name=first_name, last_name="")

        analytics_logs = ProfileAnalyticsLog.objects.filter(profile=profile)

        analytics_logs_name = ProfileAnalyticsLog.objects.filter(
            profile=profile, field="first_name"
        )
        analytics_logs_is_approved = ProfileAnalyticsLog.objects.filter(
            profile=profile, field="is_approved"
        )
        analytics_logs_visibility = ProfileAnalyticsLog.objects.filter(
            profile=profile, field="visibility"
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
        analytics_logs_allow_messaging = ProfileAnalyticsLog.objects.filter(
            profile=profile, field="allow_messaging"
        )

        self.assertEqual(first_name, analytics_logs_name.first().new_value)
        self.assertEqual("True", analytics_logs_is_approved.first().new_value)
        self.assertEqual("private", analytics_logs_visibility.first().new_value)
        self.assertEqual("user1", analytics_logs_slug.first().new_value)
        self.assertEqual(str(profile.id), analytics_logs_id.first().new_value)
        self.assertEqual(str(profile.user), analytics_logs_user_id.first().new_value)
        self.assertEqual("False", analytics_logs_email_visible.first().new_value)
        self.assertEqual(13, len(analytics_logs))
        self.assertEqual("True", analytics_logs_allow_messaging.first().new_value)
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

    def test_groups_logging(self):
        profile = self.gen.profile()
        groups_initial = [self.gen.group(), self.gen.group(), self.gen.group()]
        profile.local_groups.set(groups_initial)
        group_log = ProfileAnalyticsLog.objects.get(
            field="local_groups", old_value="[]"
        )
        for group in groups_initial:
            self.assertIn(group.name, group_log.new_value)

        groups_new: List[LocalGroup] = groups_initial[1:]
        profile.local_groups.set(groups_new)
        self.assertEqual(
            ProfileAnalyticsLog.objects.filter(field="local_groups").count(), 2
        )
        group_log_last = (
            ProfileAnalyticsLog.objects.filter(field="local_groups")
            .order_by("time")
            .last()
        )
        for group in groups_initial:
            self.assertIn(group.name, group_log_last.old_value)
        for group in groups_new:
            self.assertIn(group.name, group_log_last.new_value)

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
        profile = self.gen.profile()

        profile.first_name = "User1New"
        profile.cause_areas = [CauseArea.BUILDING_EA_COMMUNITIES]
        profile.save()

        analytics_logs_name_updated = ProfileAnalyticsLog.objects.filter(
            profile=profile, field="first_name", action="Update"
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
