import uuid
from datetime import datetime

import pytz
from django_enumfield import enum
from django.core.cache import cache
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver

from eahub.profiles.models import Profile, ProfileAnalyticsLog, CauseArea, GivingPledge, ExpertiseArea

profile_fields_to_ignore = ["_state", "_django_cleanup_original_cache"]
profile_fields_enums_map = {
    "cause_areas": CauseArea,
    "giving_pledges": GivingPledge,
    "expertise_areas": ExpertiseArea
}


def save_logs_for_new_profile(instance):
    action_uuid = uuid.uuid4()
    time = datetime.utcnow().replace(tzinfo=pytz.utc)
    for (field, value) in instance.__dict__.items():
        if (value and field not in profile_fields_to_ignore) or value is False:
            print(field)
            analytics = ProfileAnalyticsLog()
            analytics.profile = instance
            analytics.time = time
            analytics.action = "Create"
            analytics.field = field
            analytics.value = convert_value_to_printable(value, field)
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
            analytics.value = convert_value_to_printable(value, field)
            analytics.old_value = convert_value_to_printable(value, field)
            analytics.action_uuid = action_uuid
            analytics.save()


def convert_value_to_printable(value, field):
    if value is None:
        return ""
    if type(value) is not list:
        return value
    elif len(value) == 0:
        return ""
    elif field in profile_fields_enums_map.keys():
        return [profile_fields_enums_map[field].get(x).label for x in value]
    else:
        raise Exception(f"Value {value} cannot be made printable")


@receiver(post_save, sender=Profile)
def clear_the_cache(**kwargs):
    cache.clear()


@receiver(pre_save, sender=Profile)
def on_profile_change(**kwargs):
    instance = kwargs["instance"]
    if instance.id is not None:
        previous = Profile.objects.get(id=instance.id)
        save_logs_for_profile_update(instance, previous)
    if "created" in kwargs.keys() and kwargs["created"]:
        save_logs_for_new_profile(instance)


@receiver(m2m_changed, sender=Profile.local_groups.through)
def membership_updated(**kwargs):
    print("Membership")
    print(**kwargs)
    on_profile_change(**kwargs)
