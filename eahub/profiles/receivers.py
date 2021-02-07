import logging
import uuid

from django.core.cache import cache
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from eahub.base.models import User
from eahub.profiles.models import (
    CauseArea,
    ExpertiseArea,
    GivingPledge,
    OrganisationalAffiliation,
    Profile,
    ProfileAnalyticsLog,
)

logger = logging.getLogger(__name__)

profile_fields_to_ignore_on_creation = ["local_groups"]
profile_fields_enums_map = {
    "cause_areas": CauseArea,
    "giving_pledges": GivingPledge,
    "expertise_areas": ExpertiseArea,
    "organisational_affiliations": OrganisationalAffiliation,
}


def save_logs_for_new_profile(instance: Profile):
    action_uuid = uuid.uuid4()
    time = timezone.now()
    for field in instance._meta.get_fields():
        try:
            value = getattr(instance, field.name)
        except AttributeError:
            continue
        if (
            value and field.name not in profile_fields_to_ignore_on_creation
        ) or value is False:
            log = ProfileAnalyticsLog()
            log.profile = instance
            log.field = field.name
            log.action = "Create"
            log.old_value = ""
            log.new_value = convert_value_to_printable(value, field.name)
            log.time = time
            log.action_uuid = action_uuid
            log.save()


def save_logs_for_profile_update(instance_new: Profile, instance_old: Profile):
    action_uuid = uuid.uuid4()
    time = timezone.now()
    for field in instance_new._meta.get_fields():
        try:
            value_new = getattr(instance_new, field.name)
            value_old = getattr(instance_old, field.name)
        except AttributeError:
            continue
        if value_new != value_old:
            log = ProfileAnalyticsLog()
            log.profile = instance_new
            log.field = field.name
            log.action = "Update"
            log.old_value = convert_value_to_printable(value_old, field.name)
            log.new_value = convert_value_to_printable(value_new, field.name)
            log.time = time
            log.action_uuid = action_uuid
            log.save()


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
    try:
        if "created" in kwargs.keys() and kwargs["created"]:
            save_logs_for_new_profile(kwargs["instance"])
    except:
        logger.exception("Profile creation logging failed")


@receiver(pre_save, sender=Profile)
def on_profile_change(**kwargs):
    try:
        instance = kwargs["instance"]
        if instance.id is not None:
            previous = Profile.objects.get(id=instance.id)
            save_logs_for_profile_update(instance, previous)
    except:
        logger.exception("Profile update logging failed")


@receiver(pre_save, sender=User)
def on_user_change(**kwargs):
    try:
        instance_new: User = kwargs["instance"]
        is_change_action = instance_new.id is not None
        if is_change_action and instance_new.has_profile():
            instance_old: User = User.objects.get(id=instance_new.id)
            action_uuid = uuid.uuid4()
            time = timezone.now()
            for field in instance_new._meta.get_fields():
                try:
                    value_new = getattr(instance_new, field.name)
                    value_old = getattr(instance_old, field.name)
                except AttributeError:
                    continue
                if value_old != value_new:
                    ProfileAnalyticsLog.objects.create(
                        action_uuid=action_uuid,
                        time=time,
                        action="Update",
                        old_value='',
                        new_value='',
                        profile=instance_new.profile,
                        field=field.name,
                    )
    except:
        logger.exception("User update logging failed")
