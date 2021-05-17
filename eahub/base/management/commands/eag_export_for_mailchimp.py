from typing import List

import pandas
from allauth.account.forms import EmailAwarePasswordResetTokenGenerator
from allauth.account.utils import user_pk_to_url_str
from django.core.management import base
from django.urls import reverse

from eahub.base.models import User


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        df_mailchimp_raw: List[list] = []
        token_generator = EmailAwarePasswordResetTokenGenerator()
        for date_str in ["03-29", "04-12"]:
            chunks_count = 28 if date_str == "03-29" else 22
            for index in range(0, chunks_count):
                df = pandas.read_csv(f"data/users-{date_str}-filtered-part{index}.csv")
                for _, row in df.iterrows():
                    user = User.objects.get(email=row["user"])
                    password_reset_link = reverse(
                        "account_reset_password_from_key",
                        kwargs=dict(
                            uidb36=user_pk_to_url_str(user),
                            key=token_generator.make_token(user),
                        ),
                    )
                    df_mailchimp_raw.append(
                        [
                            row["user"],
                            row["first_name"],
                            row["last_name"],
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
