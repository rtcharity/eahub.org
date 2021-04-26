import datetime
from typing import List

import pandas
import numpy
import pytz
from django.core.management import base

from eahub.profiles.models import Profile, ProfileAnalyticsLog


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        for date_str in ["03-29", "04-12"]:
            df = pandas.read_csv(f"data/users-{date_str}.csv")
            emails_to_import: List[str] = df["user"].to_list()
            emails_existing = Profile.objects.filter(
                user__email__in=emails_to_import
            ).values_list("user__email", flat=True)
            emails_filtered = [
                email for email in emails_to_import if email not in emails_existing
            ]
            df_only_created = df.loc[df["user"].isin(emails_filtered)]
            chunks_amount = len(df_only_created) // 25

            for chunk_index, chunk in enumerate(
                numpy.array_split(df_only_created, chunks_amount)
            ):
                chunk.to_csv(f"data/users-{date_str}-filtered-part{chunk_index}.csv")

            count = Profile.objects.filter(user__email__in=emails_to_import).count()
            print("existing:", count)

            eag_event_announcement = datetime.datetime(2021, 2, 10, tzinfo=pytz.utc)
            eag_event_start = datetime.datetime(2021, 3, 19, tzinfo=pytz.utc)
            count = Profile.objects.filter(
                user__email__in=emails_to_import, user__date_joined__lt=eag_event_start
            ).count()
            print("before event start:", count)

            count = Profile.objects.filter(
                user__email__in=emails_to_import,
                user__date_joined__lt=eag_event_announcement,
            ).count()
            print("before event announcement:", count)

            count = Profile.objects.filter(
                user__email__in=emails_to_import,
                user__date_joined__lt=datetime.datetime(2021, 1, 1, tzinfo=pytz.utc),
            ).count()
            print("before 2021:", count)

            count = (
                ProfileAnalyticsLog.objects.filter(
                    profile__user__email__in=emails_to_import,
                    time__gt=eag_event_start,
                    time__lt=datetime.datetime.now(tz=pytz.utc),
                )
                .values("profile__user__email")
                .distinct()
                .count()
            )
            print("updated after the event:", count)
