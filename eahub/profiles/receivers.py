import uuid
from datetime import datetime

import pytz
from django.core.cache import cache
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from eahub.profiles.models import Profile, ProfileAnalyticsLog

profile_fields_to_ignore = ["_state", "_django_cleanup_original_cache"]


def save_logs_for_new_profile(instance):
    action_uuid = uuid.uuid4()
    time = datetime.utcnow().replace(tzinfo=pytz.utc)
    for (field, value) in instance.__dict__.items():
        if (value and field not in profile_fields_to_ignore) or value is False:
            analytics = ProfileAnalyticsLog()
            analytics.profile = instance
            analytics.time = time
            analytics.action = "Create"
            analytics.field = field
            analytics.value = value
            analytics.old_value = ""
            analytics.action_uuid = action_uuid
            analytics.save()


def save_logs_for_profile_update(instance, previous):
    new_fields = instance.__dict__.items()
    action_uuid = uuid.uuid4()
    time = datetime.utcnow().replace(tzinfo=pytz.utc)
    for field, value in new_fields:
        old_value = previous.__dict__[field]
        if value != old_value and field not in profile_fields_to_ignore:
            analytics = ProfileAnalyticsLog()
            analytics.profile = instance
            analytics.time = time
            analytics.action = "Update"
            analytics.field = field
            analytics.value = value if value is not None else ""
            analytics.old_value = old_value if old_value is not None else ""
            analytics.action_uuid = action_uuid
            analytics.save()


@receiver(post_save, sender=Profile)
def clear_the_cache(**kwargs):
    cache.clear()


@receiver(pre_save, sender=Profile)
def on_change(**kwargs):
    instance = kwargs["instance"]
    if instance.id is not None:
        previous = Profile.objects.get(id=instance.id)
        save_logs_for_profile_update(instance, previous)


@receiver(post_save, sender=Profile)
def save_new_profile_to_analytics(**kwargs):
    if kwargs["created"]:
        save_logs_for_new_profile(kwargs["instance"])
