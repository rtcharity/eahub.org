import logging
import uuid
from typing import Any, Union
from typing import Set

from django.core.cache import cache
from django.db.models import ManyToManyField
from django.db.models.base import ModelBase
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from eahub.base.models import User
from eahub.localgroups.models import LocalGroup
from eahub.profiles.legacy import (
    CauseArea,
    ExpertiseArea,
    GivingPledge,
    OrganisationalAffiliation,
)
from eahub.profiles.models import Membership
from eahub.profiles.models import Profile, ProfileAnalyticsLog, ProfileTag


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Profile)
def on_profile_save_clear_cache(**kwargs):
    cache.clear()


@receiver(post_save, sender=Profile)
def on_profile_creation(**kwargs):
    try:
        if "created" in kwargs.keys() and kwargs["created"]:
            _save_logs_for_profile_creation(kwargs["instance"])
    except Exception:
        logger.exception("Profile creation logging failed")


@receiver(pre_save, sender=Profile)
def on_profile_change(**kwargs):
    try:
        instance = kwargs["instance"]
        if instance.id is not None:
            instance_old = Profile.objects.get(id=instance.id)
            _save_logs_for_profile_update(instance, instance_old)
    except Exception:
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
    except Exception:
        logger.exception("User update logging failed")


@receiver(m2m_changed, sender=Profile.local_groups.through)
def log_group_update_on_m2m_change(
    sender: Membership,
    instance: Profile,
    model: ModelBase,
    pk_set: Set[int],
    action: str,
    **kwargs,
):
    if action == "pre_add":
        ProfileAnalyticsLog.objects.create(
            action_uuid=uuid.uuid4(),
            time=timezone.now(),
            action="Update",
            old_value=instance.get_local_groups_formatted(),
            new_value=[
                group.name for group in LocalGroup.objects.filter(pk__in=pk_set)
            ],
            profile=instance,
            field="local_groups",
        )
    if action == "pre_remove":
        local_groups_pks_old = set(instance.local_groups.values_list("pk", flat=True))
        local_groups_pks_removed = pk_set
        local_groups_pks_new = local_groups_pks_old - local_groups_pks_removed
        ProfileAnalyticsLog.objects.create(
            action_uuid=uuid.uuid4(),
            time=timezone.now(),
            action="Update",
            old_value=instance.get_local_groups_formatted(),
            new_value=[
                group.name
                for group in LocalGroup.objects.filter(pk__in=local_groups_pks_new)
            ],
            profile=instance,
            field="local_groups",
        )


def reindex_algolia_on_m2m_change(sender, instance: Profile, **kwargs):
    try:
        instance.save()
    except:
        logger.exception(f"Algolia tag reindexing failed for {type(instance)}")


def log_profile_tag_update(sender, instance: Profile, **kwargs):
    action = kwargs["action"]
    if action == "post_add" or action == "post_remove":
        remote_field_name: str = sender.profile.field.opts.model_name
        field_name = remote_field_name.replace("profile_", "")
        ProfileAnalyticsLog.objects.create(
            action_uuid=uuid.uuid4(),
            time=timezone.now(),
            action="Update",
            old_value="",
            new_value="",
            profile=instance,
            field=field_name,
        )


for tag_m2m_rel in [
    Profile.tags_generic.through,
    Profile.tags_cause_area.through,
    Profile.tags_cause_area_expertise.through,
    Profile.tags_expertise_area.through,
    Profile.tags_organisational_affiliation.through,
    Profile.tags_pledge.through,
    Profile.tags_speech_topic.through,
    Profile.tags_ea_involvement.through,
    Profile.tags_event_attended.through,
    Profile.tags_career_stage.through,
    Profile.tags_university.through,
    Profile.tags_affiliation.through,
]:
    m2m_changed.connect(reindex_algolia_on_m2m_change, sender=tag_m2m_rel)
    m2m_changed.connect(log_profile_tag_update, sender=tag_m2m_rel)


m2m_changed.connect(reindex_algolia_on_m2m_change, sender=ProfileTag.types.through)


def _save_logs_for_profile_creation(instance: Profile):
    action_uuid = uuid.uuid4()
    time = timezone.now()
    for field in instance._meta.get_fields():
        try:
            value = getattr(instance, field.name)
        except AttributeError:
            continue

        if type(field) == ManyToManyField:
            continue

        if value and field.name or value is False:
            ProfileAnalyticsLog.objects.create(
                profile=instance,
                field=field.name,
                action="Create",
                old_value="",
                new_value=_convert_value_to_printable(value, field.name),
                time=time,
                action_uuid=action_uuid,
            )


def _save_logs_for_profile_update(instance_new: Profile, instance_old: Profile):
    action_uuid = uuid.uuid4()
    time = timezone.now()
    for field in instance_new._meta.get_fields():
        if type(field) == ManyToManyField:
            continue
        try:
            value_new = getattr(instance_new, field.name)
            value_old = getattr(instance_old, field.name)
        except AttributeError:
            continue
        if value_new != value_old:
            ProfileAnalyticsLog.objects.create(
                profile=instance_new,
                field=field.name,
                action="Update",
                old_value=_convert_value_to_printable(value_old, field.name),
                new_value=_convert_value_to_printable(value_new, field.name),
                time=time,
                action_uuid=action_uuid,
            )


def _save_logs_for_profile_user_update(user_old: User, user_new: User):
    action_uuid = uuid.uuid4()
    time = timezone.now()
    for field in user_new._meta.get_fields():
        if type(field) == ManyToManyField:
            continue

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
                value_old_formatted = _convert_value_to_printable(value_old, field.name)
            ProfileAnalyticsLog.objects.create(
                action_uuid=action_uuid,
                time=time,
                action="Update",
                old_value=value_old_formatted,
                new_value="[protected]" if is_must_protect_password else value_new,
                profile=user_new.profile,
                field=field.name,
            )


def _convert_value_to_printable(value: Any, field: str) -> Union[str, list]:
    profile_fields_enums_map = {
        "cause_areas": CauseArea,
        "giving_pledges": GivingPledge,
        "expertise_areas": ExpertiseArea,
        "organisational_affiliations": OrganisationalAffiliation,
    }
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
