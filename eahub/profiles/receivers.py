import logging
import uuid
from typing import Any, Union

from django.core.cache import cache
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from eahub.base.models import User
from eahub.profiles.legacy import (
    CauseArea,
    ExpertiseArea,
    GivingPledge,
    OrganisationalAffiliation,
)
from eahub.profiles.models import Profile, ProfileAnalyticsLog, ProfileTag

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


def _save_logs_for_profile_user_update(user_old: User, user_new: User):
    action_uuid = uuid.uuid4()
    time = timezone.now()
    for field in user_new._meta.get_fields():
        try:
            value_new = getattr(user_new, field.name)
            value_old = getattr(user_old, field.name)
        except AttributeError:
            continue
        if value_new != value_old:
            is_must_protect_password = field.name == "password"
            if is_must_protect_password and value_old != "":
                value_old_formatted = "[protected]"
            else:
                value_old_formatted = convert_value_to_printable(value_old, field.name)
            ProfileAnalyticsLog.objects.create(
                action_uuid=action_uuid,
                time=time,
                action="Update",
                old_value=value_old_formatted,
                new_value="[protected]" if is_must_protect_password else value_new,
                profile=user_new.profile,
                field=field.name,
            )


def convert_value_to_printable(value: Any, field: str) -> Union[str, list]:
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
        user_new: User = kwargs["instance"]
        is_change_action = user_new.id is not None
        if is_change_action and user_new.has_profile():
            _save_logs_for_profile_user_update(
                user_old=User.objects.get(id=user_new.id),
                user_new=user_new,
            )
    except:
        logger.exception("User update logging failed")


@receiver(m2m_changed, sender=ProfileTag.types.through)
def reindex_on_tag_types_change(sender, instance: ProfileTag, **kwargs):
    try:
        instance.save()
    except:
        logger.exception("Algolia tag types reindexing failed")


def reindex_profile_on_tags_change(sender, instance: Profile, **kwargs):
    try:
        instance.save()
    except:
        logger.exception("Algolia tag reindexing failed")


# fmt: off
m2m_changed.connect(reindex_profile_on_tags_change, sender=Profile.tags_generic.through)
m2m_changed.connect(reindex_profile_on_tags_change, sender=Profile.tags_cause_area.through)
m2m_changed.connect(reindex_profile_on_tags_change, sender=Profile.tags_expertise_area.through)
m2m_changed.connect(reindex_profile_on_tags_change, sender=Profile.tags_organisational_affiliation.through)
m2m_changed.connect(reindex_profile_on_tags_change, sender=Profile.tags_pledge.through)
m2m_changed.connect(reindex_profile_on_tags_change, sender=Profile.tags_speech_topic.through)
