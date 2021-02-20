import autoslug.fields
import django.contrib.postgres.fields
import django.db.models.deletion
import django_enumfield.db.fields
import sorl.thumbnail.fields
from django.conf import settings
from django.db import migrations, models
from django_upload_path import upload_path

import eahub.profiles.legacy
import eahub.profiles.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False, populate_from="name", unique=True
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                (
                    "image",
                    sorl.thumbnail.fields.ImageField(
                        blank=True,
                        upload_to=upload_path.auto_cleaned_path_stripped_uuid4,
                    ),
                ),
                ("city_or_town", models.CharField(blank=True, max_length=100)),
                ("country", models.CharField(blank=True, max_length=100)),
                ("lat", models.FloatField(blank=True, default=None, null=True)),
                ("lon", models.FloatField(blank=True, default=None, null=True)),
                (
                    "cause_areas",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=django_enumfield.db.fields.EnumField(
                            default=1, enum=eahub.profiles.legacy.CauseArea
                        ),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
                (
                    "available_to_volunteer",
                    models.BooleanField(blank=True, default=None, null=True),
                ),
                (
                    "open_to_job_offers",
                    models.BooleanField(blank=True, default=None, null=True),
                ),
                (
                    "expertise_areas",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=django_enumfield.db.fields.EnumField(
                            default=1, enum=eahub.profiles.legacy.ExpertiseArea
                        ),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
                (
                    "available_as_speaker",
                    models.BooleanField(blank=True, default=None, null=True),
                ),
                ("summary", models.TextField(blank=True)),
                (
                    "giving_pledges",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=django_enumfield.db.fields.EnumField(
                            default=1, enum=eahub.profiles.legacy.GivingPledge
                        ),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
                ("subscribed_to_email_updates", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        )
    ]
