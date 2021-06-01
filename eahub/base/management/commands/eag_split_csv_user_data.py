from typing import List

import pandas
import numpy
from django.core.management import base

from eahub.profiles.models import Profile


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        df_to_override = pandas.read_csv(f"data/users-to-override.csv")
        emails_to_override: List[str] = df_to_override["email"].to_list()

        for date_str in ["03-29", "04-12"]:
            df = pandas.read_csv(f"data/users-{date_str}.csv")
            emails_to_import: List[str] = df["user"].to_list()
            emails_existing = Profile.objects.filter(
                user__email__in=emails_to_import
            ).values_list("user__email", flat=True)
            emails_existing = [email for email in emails_existing]

            emails_filtered = []
            for email in emails_to_import:
                if email not in emails_existing or email in emails_to_override:
                    emails_filtered.append(email)

            df_to_import = df.loc[df["user"].isin(emails_filtered)]
            print(df.count())
            print(df_to_import.count())
            chunks_amount = len(df_to_import) // 25

            for chunk_index, chunk in enumerate(
                numpy.array_split(df_to_import, chunks_amount)
            ):
                chunk.to_csv(f"data/users-{date_str}-filtered-part{chunk_index}.csv")
