import csv

from allauth.account.forms import EmailAwarePasswordResetTokenGenerator
from allauth.account.utils import user_pk_to_url_str
from django.core.management import base
from django.urls import reverse

from eahub.profiles.models import Profile


class Command(base.BaseCommand):
    help = "Outputs a CSV of reset links for passwordless users to stdout"

    def handle(self, *args, **options):
        self.stdout.ending = None
        writer = csv.writer(self.stdout)
        writer.writerow(["Email Address", "Name", "One-Time Login Link"])
        token_generator = EmailAwarePasswordResetTokenGenerator()
        for profile in Profile.objects.select_related("user")[:10]:
            user = profile.user
            writer.writerow(
                [
                    user.email,
                    profile.get_full_name(),
                    reverse(
                        "account_reset_password_from_key",
                        kwargs=dict(
                            uidb36=user_pk_to_url_str(user),
                            key=token_generator.make_token(user),
                        ),
                    ),
                ]
            )
