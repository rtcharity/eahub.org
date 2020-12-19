from django.test import TestCase

from eahub.base.models import User
from eahub.localgroups.models import LocalGroup, Organisership
from eahub.profiles.models import Profile


class LocalGroupTestCase(TestCase):
    def test_organisers_names(self):
        local_group = LocalGroup()
        local_group.save()

        user1 = User()
        user1.email = "user1@email.com"
        user1.save()

        user2 = User()
        user2.email = "user2@email.com"
        user2.save()

        profile1 = Profile()
        name1 = "Peter"
        profile1.name = name1
        profile1.user = user1
        profile1.save()

        profile2 = Profile()
        name2 = "Mary"
        profile2.name = name2
        profile2.user = user2
        profile2.save()

        o1 = Organisership(user=user1, local_group=local_group)
        o1.save()

        o2 = Organisership(user=user2, local_group=local_group)
        o2.save()

        organiser_names = local_group.organisers_names()

        self.assertEqual(f"{name1}, {name2}", organiser_names)

    def test_organisers_names_handles_users_without_profiles(self):
        local_group = LocalGroup()
        local_group.save()
        user_without_profile = User()
        user_without_profile.save()
        o = Organisership(user=user_without_profile, local_group=local_group)
        o.save()

        organisers_names = local_group.organisers_names()

        self.assertEqual("User profile missing", organisers_names)

    def test_get_exportable_field_names(self):
        actual = LocalGroup.get_exportable_field_names()

        expected_field_names = [
            "id",
            "slug",
            "is_public",
            "name",
            "is_active",
            "organisers_freetext",
            "local_group_types",
            "city_or_town",
            "region",
            "country",
            "lat",
            "lon",
            "website",
            "other_website",
            "facebook_group",
            "facebook_page",
            "email",
            "meetup_url",
            "airtable_record",
            "last_edited",
            "other_info",
            "organisers",
            "organisers_emails",
        ]

        self.assertListEqual(expected_field_names, actual)
