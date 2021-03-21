from django.db import migrations, models

import eahub.profiles.models
from eahub.profiles.models import ProfileTagType, ProfileTagTypeEnum


def create_profile_tag_types(apps, schema_editor):
    for enum_member in ProfileTagTypeEnum:
        ProfileTagType.objects.get_or_create(type=enum_member)


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0022_add_field_last_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="profile",
            options={"ordering": ["first_name", "slug"]},
        ),
        migrations.AddField(
            model_name="profile",
            name="is_hiring",
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name="profile",
            name="job_title",
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AddField(
            model_name="profile",
            name="organization",
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AddField(
            model_name="profile",
            name="study_subject",
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AddField(
            model_name="profile",
            name="tags_career_stage",
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={
                    "types__type": eahub.profiles.models.ProfileTagTypeEnum(
                        "career_stage"
                    )
                },
                related_name="tags_career_stage",
                to="profiles.ProfileTag",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="tags_ea_involvement",
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={
                    "types__type": eahub.profiles.models.ProfileTagTypeEnum(
                        "ea_involvement"
                    )
                },
                related_name="tags_ea_involvement",
                to="profiles.ProfileTag",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="tags_event_attended",
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={
                    "types__type": eahub.profiles.models.ProfileTagTypeEnum(
                        "event_attended"
                    )
                },
                related_name="tags_event_attended",
                to="profiles.ProfileTag",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="tags_university",
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={
                    "types__type": eahub.profiles.models.ProfileTagTypeEnum(
                        "university"
                    )
                },
                related_name="tags_university",
                to="profiles.ProfileTag",
            ),
        ),
        migrations.RunPython(
            code=create_profile_tag_types,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
