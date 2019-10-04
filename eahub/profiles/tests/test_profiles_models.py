from django.test import TestCase
from model_mommy import mommy

from eahub.profiles.models import Profile


class ProfileTests(TestCase):
    def setUp(self):
        self.name = "Test Person"

    def test_profile_creation(self):
        profile = mommy.make("Profile", slug="slug", name="Derek Parfit")
        self.assertTrue(isinstance(profile, Profile))
        self.assertTrue(str(profile), "Derek Parfit")

    def test_geocode(self):
        profile = mommy.make(
            "Profile",
            slug=self.name,
            name=self.name,
            city_or_town="London",
            country="UK",
        )
        profile.geocode()
        self.assertAlmostEqual(profile.lat, 51.4893335)
        self.assertAlmostEqual(profile.lon, -0.144055084527687)

    def test_has_cause_area_details(self):
        profile_without_cause_area = mommy.make("Profile", slug="slug", name=self.name)
        self.assertFalse(profile_without_cause_area.has_cause_area_details())

        profile_with_cause_area = mommy.make(
            "Profile", slug="slug", name=self.name, cause_areas_other="Cause X"
        )
        self.assertTrue(profile_with_cause_area.has_cause_area_details())
