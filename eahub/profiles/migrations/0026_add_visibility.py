# Generated by Django 2.2.17 on 2021-04-18 13:34

import django.core.validators
from django.db import migrations, models
from eahub.profiles.models import VisibilityEnum
import eahub.profiles.validators
import enumfields.fields


def migrate_is_public_to_visibility(apps, schema_editor):
    Profile = apps.get_model("profiles", "Profile")
    for profile in Profile.objects.all():
        if profile.is_public:
            profile.visibility = VisibilityEnum.PUBLIC
        else:
            profile.visibility = VisibilityEnum.PRIVATE
        profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0025_add_fields_tags_cause_area_expertise_and_tags_affiliation'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='visibility',
            field=enumfields.fields.EnumField(default='private', enum=eahub.profiles.models.VisibilityEnum, max_length=16),
        ),
        migrations.RunPython(migrate_is_public_to_visibility, migrations.RunPython.noop),
    ]
