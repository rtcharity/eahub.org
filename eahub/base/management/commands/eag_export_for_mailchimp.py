from typing import List

import pandas
from allauth.account.forms import EmailAwarePasswordResetTokenGenerator
from allauth.account.utils import user_pk_to_url_str
from django.core.management import base
from django.urls import reverse

from eahub.profiles.models import Profile


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        df_mailchimp_raw: List[list] = []
        token_generator = EmailAwarePasswordResetTokenGenerator()
        with open("data/mailchimp-emails.csv") as file:
            for line in file:
                print(line)
                profile = Profile.objects.get(user__email=line.strip())
                password_reset_link = reverse(
                    "account_reset_password_from_key",
                    kwargs=dict(
                        uidb36=user_pk_to_url_str(profile.user),
                        key=token_generator.make_token(profile.user),
                    ),
                )
                df_mailchimp_raw.append(
                    [
                        profile.user.email,
                        profile.first_name,
                        profile.last_name,
                        f"https://eahub.org{password_reset_link}",
                        "EA Global Reconnect",
                        "EAGR - 2021.05.17",
                    ]
                )
        df = pandas.DataFrame(
            df_mailchimp_raw,
            columns=[
                "Email Address",
                "First Name",
                "Last Name",
                "Activation Link",
                "Event Source",
                "TAGS",
            ],
        )
        df.to_csv(f"data/eag-mailchimp-05-17.csv", index=False)
