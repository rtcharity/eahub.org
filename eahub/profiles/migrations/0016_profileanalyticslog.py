# Generated by Django 2.2.16 on 2021-01-01 19:49

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("profiles", "0015_profile_email_visible")]

    operations = [
        migrations.CreateModel(
            name="ProfileAnalyticsLog",
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
                ("time", models.DateTimeField()),
                ("field", models.CharField(max_length=255)),
                ("action", models.CharField(max_length=255)),
                ("action_uuid", models.UUIDField(default=uuid.uuid4)),
                ("old_value", models.TextField()),
                ("new_value", models.TextField()),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.Profile",
                    ),
                ),
            ],
        )
    ]
