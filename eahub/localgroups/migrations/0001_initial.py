import autoslug.fields
import django.core.validators
import django.db.models.deletion
import django_enumfield.db.fields
from django.conf import settings
from django.db import migrations, models

import eahub.localgroups.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="LocalGroup",
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
                ("name", models.CharField(max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "local_group_type",
                    django_enumfield.db.fields.EnumField(
                        blank=True,
                        default=None,
                        enum=eahub.localgroups.models.LocalGroupType,
                        null=True,
                    ),
                ),
                ("city_or_town", models.CharField(blank=True, max_length=100)),
                ("country", models.CharField(blank=True, max_length=100)),
                ("lat", models.FloatField(blank=True, default=None, null=True)),
                ("lon", models.FloatField(blank=True, default=None, null=True)),
                ("website", models.URLField(blank=True)),
                ("facebook_group", models.URLField(blank=True)),
                ("facebook_page", models.URLField(blank=True)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("meetup_url", models.URLField(blank=True)),
                (
                    "airtable_record",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=255,
                        null=True,
                        unique=True,
                        validators=[django.core.validators.MinLengthValidator(1)],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Organisership",
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
                    "local_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="localgroups.LocalGroup",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="localgroup",
            name="organisers",
            field=models.ManyToManyField(
                blank=True,
                through="localgroups.Organisership",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
