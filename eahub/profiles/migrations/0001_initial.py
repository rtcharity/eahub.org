from django.contrib.auth import validators as auth_validators
from django.contrib.postgres import fields as postgres_fields
from django.contrib.postgres.fields import citext
from django.contrib.postgres import operations as postgres_operations
from django.db import migrations
from django.db import models
from django.utils import timezone
from django_upload_path import upload_path
from sorl.thumbnail import fields as thumbnail_fields

from .. import models as profiles_models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("auth", "0009_alter_user_last_name_max_length")]

    operations = [
        postgres_operations.CITextExtension(),
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[auth_validators.UnicodeUsernameValidator()],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=30, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=timezone.now, verbose_name="date joined"
                    ),
                ),
                ("email", citext.CIEmailField(max_length=254, unique=True)),
                ("summary", models.TextField(blank=True, null=True)),
                (
                    "image",
                    thumbnail_fields.ImageField(
                        blank=True,
                        upload_to=upload_path.auto_cleaned_path_stripped_uuid4,
                    ),
                ),
                (
                    "city_or_town",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "lat",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        max_digits=9,
                        null=True,
                        verbose_name="latitude",
                    ),
                ),
                (
                    "lon",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        max_digits=9,
                        null=True,
                        verbose_name="longitude",
                    ),
                ),
                ("gdpr_confirmed", models.BooleanField(default=True)),
                (
                    "cause_areas",
                    postgres_fields.ArrayField(
                        base_field=models.CharField(
                            blank=True,
                            choices=[
                                ("GLOBAL_POVERTY", "Global Poverty"),
                                ("ANIMAL_WELFARE_AND_RIGHTS", "Animal Welfare/Rights"),
                                ("LONG_TERM_FUTURE", "Long-term Future"),
                                ("CAUSE_PRIORITISATION", "Cause Prioritisation"),
                                ("META", "Meta"),
                                ("OTHER", "Other"),
                            ],
                            max_length=25,
                            null=True,
                        ),
                        default=list,
                        size=None,
                    ),
                ),
                ("cause_areas_other", models.TextField(blank=True, null=True)),
                (
                    "available_to_volunteer",
                    models.BooleanField(default=None, null=True),
                ),
                (
                    "giving_pledge",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("", "No"),
                            ("GIVING_WHAT_WE_CAN", "Giving What We Can"),
                            ("THE_LIFE_YOU_CAN_CHANGE", "The Life You Can Save"),
                            ("ONE_FOR_THE_WORLD", "One for the World"),
                            ("OTHER", "Other"),
                        ],
                        max_length=23,
                        null=True,
                    ),
                ),
                ("giving_pledge_other", models.TextField(blank=True, null=True)),
                ("open_to_job_offers", models.BooleanField(default=None, null=True)),
                (
                    "expertise",
                    postgres_fields.ArrayField(
                        base_field=models.CharField(
                            blank=True,
                            choices=[
                                ("MANAGEMENT", "Management"),
                                ("OPERATIONS", "Operations"),
                                ("RESEARCH", "Research"),
                                ("GOVERNMENT_AND_POLICY", "Government and policy"),
                                ("ENTREPRENEURSHIP", "Entrepreneurship"),
                                ("SOFTWARE_ENGINEERING", "Software engineering"),
                                ("AI_TECHNICAL_EXPERTISE", "AI technical expertise"),
                                (
                                    "MATH_QUANT_STATS_EXPERTISE",
                                    "Math, quant, stats expertise",
                                ),
                                (
                                    "ECONOMICS, QUANTITATIVE SOCIAL SCIENCE",
                                    "Economics, quantitative social science",
                                ),
                                ("MOVEMENT_BUILDING", "Movement building"),
                                ("COMMUNICATIONS", "Communications"),
                                ("OTHER", "Other"),
                            ],
                            max_length=38,
                            null=True,
                        ),
                        default=list,
                        size=None,
                    ),
                ),
                ("expertise_other", models.TextField(blank=True, null=True)),
                ("available_as_speaker", models.BooleanField(default=None, null=True)),
                ("topics_i_speak_about", models.TextField(blank=True, null=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={"verbose_name": "Profile", "verbose_name_plural": "Profiles"},
            managers=[("objects", profiles_models.ProfileManager())],
        ),
    ]
