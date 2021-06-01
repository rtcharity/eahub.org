import django.core.validators
from django.db import migrations, models

import eahub.profiles.validators


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0021_alter_bool_fields_by_preventing_null"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile",
            old_name="name",
            new_name="first_name",
        ),
        migrations.AddField(
            model_name="profile",
            name="last_name",
            field=models.CharField(
                default="",
                max_length=200,
                validators=[eahub.profiles.validators.validate_sluggable_name],
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="profile",
            name="allow_messaging",
            field=models.BooleanField(
                default=True, verbose_name="Allow approved users to message me"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="available_as_speaker",
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name="profile",
            name="available_to_volunteer",
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name="profile",
            name="facebook_url",
            field=models.URLField(blank=True, max_length=400, verbose_name="Facebook"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="is_public",
            field=models.BooleanField(
                default=True,
                help_text="Unchecking this will completely conceal your profile",
                verbose_name="Public profile",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="linkedin_url",
            field=models.URLField(blank=True, max_length=400, verbose_name="Linkedin"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="open_to_job_offers",
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name="profile",
            name="personal_website_url",
            field=models.URLField(
                blank=True, max_length=400, verbose_name="Personal website"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="summary",
            field=models.TextField(
                blank=True,
                validators=[django.core.validators.MaxLengthValidator(6000)],
                verbose_name="Bio",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="topics_i_speak_about",
            field=models.TextField(
                blank=True,
                validators=[django.core.validators.MaxLengthValidator(2000)],
                verbose_name="Topics I speak about other",
            ),
        ),
    ]
