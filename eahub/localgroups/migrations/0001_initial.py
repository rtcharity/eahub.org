from django.conf import settings
from django.core import validators
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Group",
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
                ("name", models.CharField(max_length=100)),
                (
                    "group_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("COUNTRY", "Country"),
                            ("CITY", "City"),
                            ("UNIVERSITY", "University"),
                            ("OTHER", "Other"),
                        ],
                        max_length=10,
                        null=True,
                    ),
                ),
                ("group_type_other", models.TextField(blank=True, null=True)),
                ("summary", models.TextField(blank=True, null=True)),
                (
                    "city_or_town",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
                ("website", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "facebook_group",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "facebook_page",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("email", models.CharField(blank=True, max_length=200, null=True)),
                ("meetup_details", models.TextField(blank=True, null=True)),
                ("meetups_per_month", models.IntegerField(blank=True, null=True)),
                ("meetup_url", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "lat",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=9, null=True
                    ),
                ),
                (
                    "lon",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=9, null=True
                    ),
                ),
                (
                    "airtable_record",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=255,
                        null=True,
                        unique=True,
                        validators=[validators.MinLengthValidator(1)],
                    ),
                ),
                ("donations", models.TextField(blank=True, null=True)),
                ("links", models.TextField(blank=True, null=True)),
                ("images", models.TextField(blank=True, null=True)),
                ("edit_history", models.TextField(default="[]")),
                (
                    "organisers",
                    models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
                ),
            ],
        )
    ]
