import django.core.validators
from django.db import migrations, models
import eahub.profiles.models
from eahub.profiles.models import ProfileTagTypeEnum


def create_profile_tag_types(apps, schema_editor):
    ProfileTagType = apps.get_model("profiles", "ProfileTagType")

    for enum_member in ProfileTagTypeEnum:
        ProfileTagType.objects.get_or_create(type=enum_member)

    tag_cause_area_expertise_type = ProfileTagType.objects.get(
        type=ProfileTagTypeEnum.CAUSE_AREA_EXPERTISE
    )
    ProfileTag = apps.get_model("profiles", "ProfileTag")
    for tag in ProfileTag.objects.filter(types__type=ProfileTagTypeEnum.CAUSE_AREA):
        tag.types.add(tag_cause_area_expertise_type)


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0024_migrate_old_name_field"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="tags_affiliation",
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={
                    "types__type": eahub.profiles.models.ProfileTagTypeEnum(
                        "affiliation"
                    )
                },
                related_name="tags_affiliation",
                to="profiles.ProfileTag",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="tags_cause_area_expertise",
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={
                    "types__type": eahub.profiles.models.ProfileTagTypeEnum(
                        "cause_area_expertise"
                    )
                },
                related_name="tags_cause_area_expertise",
                to="profiles.ProfileTag",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="allow_messaging",
            field=models.BooleanField(
                default=True,
                help_text="Your email address won't be visible to them",
                verbose_name="Allow approved users to message me",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="topics_i_speak_about",
            field=models.TextField(
                blank=True,
                validators=[django.core.validators.MaxLengthValidator(2000)],
                verbose_name="Topics I speak about",
            ),
        ),
        migrations.RunPython(create_profile_tag_types, migrations.RunPython.noop),
    ]
