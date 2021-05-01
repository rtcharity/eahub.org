from django.contrib.auth.hashers import make_password
from django.core.management import base
from faker import Faker

from eahub.base.models import User
from eahub.profiles.models import Profile, ProfileAnalyticsLog
from eahub.profiles.models import VisibilityEnum


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        profiles = (
            Profile.objects.filter(email_visible=False)
            .select_related("user")
            .values_list("id", flat=True)
        )

        profiles_to_fake = profiles[:500]
        profiles_to_delete = profiles[500:]
        fake = Faker()
        for profile_id in profiles_to_fake:
            profile = Profile.objects.get(id=profile_id)
            profile.user.email = fake.unique.email()
            profile.user.save()

        ProfileAnalyticsLog.objects.all().delete()

        User.objects.filter(profile__id__in=profiles_to_delete).delete()
        User.objects.filter(profile__visibility=VisibilityEnum.PRIVATE).delete()

        fake_password_hash = make_password("fake_password")
        User.objects.update(password=fake_password_hash)
