import datetime

import pandas as pd
import pytz
from django.core.management import base

from eahub.profiles.models import Profile, ProfileAnalyticsLog


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        df = pd.read_csv("EAG Reconnect_ Export for EA Hub - March 29 - Hub Format.csv")
        for profile in Profile.objects.filter(user__email__in=df["user"].to_list()):
            log = (
                ProfileAnalyticsLog.objects.filter(
                    profile=profile,
                    time__gt=datetime.datetime(2021, 3, 19, tzinfo=pytz.utc),
                )
                .order_by("time")
                .last()
            )
            if log:
                print(log.time)
