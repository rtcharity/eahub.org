from django.db import migrations, models

from eahub.profiles.models import Profile


def remove_nulls_from_boolean_fields(apps, schema_editor):
    Profile.objects.filter(available_as_speaker=None).update(available_as_speaker=False)
    Profile.objects.filter(open_to_job_offers=None).update(open_to_job_offers=False)
    Profile.objects.filter(available_to_volunteer=None).update(
        available_to_volunteer=False
    )


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0019_add_tags"),
    ]

    operations = [
        migrations.RunPython(
            code=remove_nulls_from_boolean_fields,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
