from typing import Any, List, Union

import django.db.models.deletion
import enumfields.fields
from django.db import migrations, models
from django_enumfield.enum import Enum as OldEnum
from enumfields import Enum

import eahub.profiles.models
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
        ("profiles", "0017_profile_offering_looking_for"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProfileTagType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    enumfields.fields.EnumField(
                        enum=ProfileTagTypeEnum,
                        max_length=128,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProfileTag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128, unique=True)),
                ("description", models.TextField(blank=True)),
                ("is_featured", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="profiles.Profile",
                    ),
                ),
                ("types", models.ManyToManyField(to="profiles.ProfileTagType")),
                (
                    "status",
                    enumfields.fields.EnumField(
                        default="approved",
                        enum=eahub.profiles.models.ProfileTagStatus,
                        max_length=64,
                    ),
                ),
                ("synonyms", models.CharField(blank=True, max_length=1024)),
            ],
        ),
        migrations.AddField(
            model_name="profile",
            name="tags_cause_area",
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={"types__type": ProfileTagTypeEnum.CAUSE_AREA},
                related_name="tags_cause_area",
                to="profiles.ProfileTag",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="tags_expertise_area",
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={"types__type": ProfileTagTypeEnum.EXPERTISE_AREA},
                related_name="tags_expertise_area",
                to="profiles.ProfileTag",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="tags_generic",
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={"types__type": ProfileTagTypeEnum.GENERIC},
                related_name="tags_generic",
                to="profiles.ProfileTag",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="tags_career_interest",
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={"types__type": ProfileTagTypeEnum.CAREER_INTEREST},
                related_name="tags_career_interest",
                to="profiles.ProfileTag",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="tags_organisational_affiliation",
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={
                    "types__type": ProfileTagTypeEnum.ORGANISATIONAL_AFFILIATION
                },
                related_name="tags_organisational_affiliation",
                to="profiles.ProfileTag",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="tags_pledge",
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={"types__type": ProfileTagTypeEnum.PLEDGE},
                related_name="tags_pledge",
                to="profiles.ProfileTag",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="tags_speech_topic",
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={"types__type": ProfileTagTypeEnum.SPEECH_TOPIC},
                related_name="tags_speech_topic",
                to="profiles.ProfileTag",
            ),
        ),
        migrations.RunPython(
            code=migrate_to_tags_from_enums,
            reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
    ]
