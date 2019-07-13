import django.contrib.postgres.fields
import django_enumfield.db.fields
from django.db import migrations

import eahub.profiles.models


class Migration(migrations.Migration):

    dependencies = [("profiles", "0010_remove_profile_subscribed_to_email_updates")]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="career_interest_areas",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=django_enumfield.db.fields.EnumField(
                    default=1, enum=eahub.profiles.models.ExpertiseArea
                ),
                blank=True,
                default=list,
                size=None,
            ),
        )
    ]
