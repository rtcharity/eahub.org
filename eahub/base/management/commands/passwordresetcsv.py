import csv

from django import urls
from django.contrib.auth import tokens
from django.core.management import base
from django.utils import encoding, http

from ....profiles import models


class Command(base.BaseCommand):
    help = "Outputs a CSV of reset links for passwordless users to stdout"

    def handle(self, *args, **options):
        self.stdout.ending = None
        writer = csv.writer(self.stdout)
        writer.writerow(["Email Address", "Name", "One-Time Login Link"])
        for profile in models.Profile.objects.select_related("user").filter(
            user__password="", user__is_active=True
        ):
            user = profile.user
            writer.writerow(
                [
                    user.email,
                    profile.get_full_name(),
                    urls.reverse(
                        "password_reset_confirm",
                        kwargs={
                            "uidb64": http.urlsafe_base64_encode(
                                encoding.force_bytes(user.pk)
                            ),
                            "token": tokens.default_token_generator.make_token(user),
                        },
                    ),
                ]
            )
