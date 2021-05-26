from eahub.base.models import User
from eahub.localgroups.models import LocalGroup, Organisership
from eahub.profiles.models import Profile, VisibilityEnum
from eahub.tests.cases import EAHubTestCase


class LocalGroupTestCase(EAHubTestCase):
    def test_organisers_names(self):
        first_name1 = "ada"
        last_name1 = "khan"
        first_name2 = "bob"
        last_name2 = "xi"

        profile1 = self.gen.profile(first_name=first_name1, last_name=last_name1)
        profile2 = self.gen.profile(first_name=first_name2, last_name=last_name2)
        local_group = self.gen.group(users=[profile1.user, profile2.user])

        organiser_names = local_group.organisers_names()

        self.assertIn(f"{first_name1} {last_name1}", organiser_names)
        self.assertIn(f"{first_name2} {last_name2}", organiser_names)

    def test_organisers_names_handles_users_without_profiles(self):
        user_without_profile = self.gen.user()
        local_group = self.gen.group(users=[user_without_profile])

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

    def test_public_and_internal_organisers(self):

        profile_public = self.gen.profile(visibility=VisibilityEnum.PUBLIC)
        profile_internal = self.gen.profile(visibility=VisibilityEnum.INTERNAL)
        profile_private = self.gen.profile(visibility=VisibilityEnum.PRIVATE)

        group = self.gen.group(users=[profile_private.user, profile_internal.user, profile_public.user])

        actual = group.public_and_internal_organisers()

        self.assertCountEqual([profile_internal, profile_public], [x.profile for x in list(actual)])




