import datetime
from typing import List

import pandas as pd
import pytz
from django.core.management import base

from eahub.profiles.models import Profile, ProfileAnalyticsLog


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        df = pd.read_csv(
            "EAG Reconnect_ Export for EA Hub - Copy of April 12 - Hub Format.csv"
        )
        emails_to_import: List[str] = df["user"].to_list()

        count = Profile.objects.filter(user__email__in=emails_to_import).count()
        print("existing:", count)
        emails_existing = Profile.objects.filter(
            user__email__in=emails_to_import
        ).values_list("user__email", flat=True)

        emails_filtered = [
            email for email in emails_to_import if email not in emails_existing
        ]
        df = df.loc[df["user"].isin(emails_filtered)]
        df.to_csv("output-04-12.csv")

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

        count = (
            ProfileAnalyticsLog.objects.filter(
                profile__user__email__in=emails_to_import,
                time__gt=eag_event_start,
                time__lt=datetime.datetime.now(tz=pytz.utc),
            )
            .values("action_uuid")
            .distinct()
            .count()
        )
        print("updated after the event:", count)
