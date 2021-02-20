from typing import Any, List, Union

from django.db import migrations
from django_enumfield.enum import Enum as OldEnum
from enumfields import Enum

from eahub.profiles.legacy import (
    CauseArea,
    ExpertiseArea,
    GivingPledge,
    OrganisationalAffiliation,
)
from eahub.profiles.models import (
    Profile,
    ProfileTag,
    ProfileTagType,
    ProfileTagTypeEnum,
)


def migrate_to_tags_from_enums(apps, schema_editor):
    for profile in Profile.objects.all():
        _migrate_enum(
            profile,
            enum_cls_old=OrganisationalAffiliation,
            field_name_old="organisational_affiliations",
            field_name_new="tags_organisational_affiliation",
            enum_types=[ProfileTagTypeEnum.ORGANISATIONAL_AFFILIATION],
        )
        _migrate_enum(
            profile,
            enum_cls_old=GivingPledge,
            field_name_old="giving_pledges",
            field_name_new="tags_pledge",
            enum_types=[ProfileTagTypeEnum.PLEDGE],
        )
        _migrate_enum(
            profile,
            enum_cls_old=CauseArea,
            field_name_old="cause_areas",
            field_name_new="tags_cause_area",
            enum_types=[
                ProfileTagTypeEnum.EXPERTISE_AREA,
                ProfileTagTypeEnum.CAUSE_AREA,
                ProfileTagTypeEnum.CAREER_INTEREST,
                ProfileTagTypeEnum.SPEECH_TOPIC,
            ],
        )
        _migrate_enum(
            profile,
            enum_cls_old=ExpertiseArea,
            field_name_old="expertise_areas",
            field_name_new="tags_expertise_area",
            enum_types=[
                ProfileTagTypeEnum.EXPERTISE_AREA,
                ProfileTagTypeEnum.CAREER_INTEREST,
                ProfileTagTypeEnum.SPEECH_TOPIC,
            ],
        )
        _migrate_enum(
            profile,
            enum_cls_old=ExpertiseArea,
            field_name_old="career_interest_areas",
            field_name_new="tags_career_interest",
            enum_types=[
                ProfileTagTypeEnum.EXPERTISE_AREA,
                ProfileTagTypeEnum.CAREER_INTEREST,
                ProfileTagTypeEnum.SPEECH_TOPIC,
            ],
        )


def _migrate_enum(
    profile: Profile,
    enum_cls_old: Union[OldEnum, Any],
    field_name_old: str,
    field_name_new: str,
    enum_types: List[Enum],
):
    tags_new = []
    for enum_key in getattr(profile, field_name_old):
        tag_types = []
        for enum_type in enum_types:
            tag_type, _ = ProfileTagType.objects.get_or_create(type=enum_type)
            tag_types.append(tag_type)
        tag, _ = ProfileTag.objects.get_or_create(name=enum_cls_old.labels[enum_key])
        tag.types.set(tag_types)
        tags_new.append(tag)

    tags_field = getattr(profile, field_name_new)
    tags_field.set(tags_new)


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0022_add_fields_for_tags"),
    ]

    operations = [
        migrations.RunPython(
            code=migrate_to_tags_from_enums, reverse_code=migrations.RunPython.noop
        ),
    ]
