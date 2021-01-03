import logging
import uuid

from django.core.cache import cache
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from eahub.profiles.models import (
    CauseArea,
    ExpertiseArea,
    GivingPledge,
    OrganisationalAffiliation,
    Profile,
    ProfileAnalyticsLog,
)

logger = logging.getLogger(__name__)

profile_fields_to_ignore = ["_state", "_django_cleanup_original_cache"]
profile_fields_enums_map = {
    "cause_areas": CauseArea,
    "giving_pledges": GivingPledge,
    "expertise_areas": ExpertiseArea,
    "organisational_affiliations": OrganisationalAffiliation,
}


def save_logs_for_new_profile(instance):
    action_uuid = uuid.uuid4()
    time = timezone.now()
    for (field, value) in instance.__dict__.items():
        if (value and field not in profile_fields_to_ignore) or value is False:
            log = ProfileAnalyticsLog()
            log.store(
                profile=instance,
                field=field,
                action="Create",
                old_value="",
                new_value=convert_value_to_printable(value, field),
                time=time,
                action_uuid=action_uuid,
            )


def save_logs_for_profile_update(instance, previous):
    new_fields = instance.__dict__.items()
    action_uuid = uuid.uuid4()
    time = timezone.now()
    for field, value in new_fields:
        old_value = previous.__dict__[field]
        if value != old_value and field not in profile_fields_to_ignore:
            log = ProfileAnalyticsLog()
            log.store(
                profile=instance,
                field=field,
                action="Update",
                old_value=convert_value_to_printable(old_value, field),
                new_value=convert_value_to_printable(value, field),
                time=time,
                action_uuid=action_uuid,
            )


def convert_value_to_printable(value, field):
    if value is None:
        return ""
    if type(value) is not list:
        return value
    elif len(value) == 0:
        return ""
    elif field in profile_fields_enums_map.keys():
        return [profile_fields_enums_map[field].get(int(x)).label for x in value]
    else:
        logger.warning(f"Value {value} cannot be made printable")
        return str(value)


@receiver(post_save, sender=Profile)
def clear_the_cache(**kwargs):
    cache.clear()


@receiver(post_save, sender=Profile)
def on_profile_creation(**kwargs):
    if "created" in kwargs.keys() and kwargs["created"]:
        save_logs_for_new_profile(kwargs["instance"])


@receiver(pre_save, sender=Profile)
def on_profile_change(**kwargs):
    instance = kwargs["instance"]
    if instance.id is not None:
        previous = Profile.objects.get(id=instance.id)
        save_logs_for_profile_update(instance, previous)
