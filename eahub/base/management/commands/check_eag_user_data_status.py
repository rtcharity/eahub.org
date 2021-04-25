import datetime
from typing import List

import pandas as pd
import pytz
from django.core.management import base

from eahub.profiles.models import Profile


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        df = pd.read_csv("eag_emails.csv")
        emails: List[str] = df["user"].to_list()

        count = Profile.objects.filter(user__email__in=emails).count()
        print("existing:", count)

        eag_event_announcement = datetime.datetime(2021, 2, 10, tzinfo=pytz.utc)
        eag_event_start = datetime.datetime(2021, 3, 19, tzinfo=pytz.utc)
        count = Profile.objects.filter(
            user__email__in=emails, user__date_joined__lt=eag_event_start
        ).count()
        print("before event start:", count)

        count = Profile.objects.filter(
            user__email__in=emails, user__date_joined__lt=eag_event_announcement
        ).count()
        print("before event announcement:", count)
