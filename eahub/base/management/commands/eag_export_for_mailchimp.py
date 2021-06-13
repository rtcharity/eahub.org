from typing import List

import pandas
from allauth.account.forms import EmailAwarePasswordResetTokenGenerator
from allauth.account.utils import user_pk_to_url_str
from django.core.management import base
from django.urls import reverse

from eahub.profiles.models import Profile
from eahub.profiles.models import VisibilityEnum


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        df_mailchimp_raw: List[list] = []
        token_generator = EmailAwarePasswordResetTokenGenerator()
        with open("data/mailchimp-emails.csv") as file:
            for line in file:
                try:
                    profile = Profile.objects.get(user__email=line.strip())
                except Profile.DoesNotExist:
                    continue

                if (
                    profile.visibility == VisibilityEnum.PRIVATE
                    and not profile.user.password
                ):
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
                            "EAGR,EAGR - 2021.06.06,EAGR-created",
                        ]
                    )
                elif (
                    profile.visibility == VisibilityEnum.PRIVATE
                    and profile.user.password
                ):
                    df_mailchimp_raw.append(
                        [
                            profile.user.email,
                            profile.first_name,
                            profile.last_name,
                            f"https://eahub.org{reverse('profiles_app:profile_update_import')}",
                            "EA Global Reconnect",
                            "EAGR,EAGR - 2021.06.06,EAGR-updated",
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
        df.to_csv(f"data/eag-mailchimp-06-06.csv", index=False)
