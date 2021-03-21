from eahub.localgroups.admin import LocalGroupResource
from eahub.localgroups.models import LocalGroup
from eahub.localgroups.models import Organisership
from eahub.profiles.models import Profile
from eahub.tests.cases import EAHubTestCase


class LocalGroupAdminTestCase(EAHubTestCase):
    def setUp(self):
        self.first_name = "Peter"
        self.local_group = LocalGroup.objects.create(id=1)

        self.profile_peter = self.gen.profile(first_name=self.first_name)
        self.profile_mary = self.gen.profile(first_name="Mary")
        self.profile_peter2 = self.gen.profile(first_name=self.first_name)

        Organisership.objects.create(
            user=self.profile_peter.user, local_group=self.local_group
        )
        Organisership.objects.create(
            user=self.profile_mary.user, local_group=self.local_group
        )

    def test_hydrate_organiser_where_users_with_same_name_and_one_already_organiser(
        self,
    ):
        organizer_found = LocalGroupResource().hydrate_organiser(
            self.first_name, row={"id": "1"}
        )
        self.assertEqual(self.profile_peter.user, organizer_found)

    def test_hydrate_organiser_where_users_with_same_name_and_already_organisers(self):
        Organisership.objects.create(
            user=self.profile_peter2.user, local_group=self.local_group
        )
        organizer_found = LocalGroupResource().hydrate_organiser(
            self.first_name, row={"id": "1"}
        )
        self.assertEqual(
            self.profile_peter2.get_full_name(),
            Profile.objects.get(user=organizer_found).get_full_name(),
        )
        self.assertEqual(self.profile_peter2.user, organizer_found)
