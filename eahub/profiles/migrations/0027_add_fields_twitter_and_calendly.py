import django.core.validators
from django.db import migrations, models

import eahub.profiles.validators


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0026_add_visibility"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="calendly_url",
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.AddField(
            model_name="profile",
            name="twitter",
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.AlterField(
            model_name="profile",
            name="city_or_town",
            field=models.CharField(blank=True, max_length=100, verbose_name="City"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="first_name",
            field=models.CharField(
                max_length=200,
                validators=[eahub.profiles.validators.validate_sluggable_name],
                verbose_name="First Name",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="is_public",
            field=models.BooleanField(
                default=True,
                help_text="Unchecking this will conceal your profile from everyone. While visible profiles are searchable on the web.",
                verbose_name="Visible profile",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="job_title",
            field=models.CharField(
                blank=True, max_length=1024, verbose_name="Job Title"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="last_name",
            field=models.CharField(
                max_length=200,
                validators=[eahub.profiles.validators.validate_sluggable_name],
                verbose_name="Last Name",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="local_groups",
            field=models.ManyToManyField(
                blank=True,
                through="profiles.Membership",
                to="localgroups.LocalGroup",
                verbose_name="EA Groups",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="personal_website_url",
            field=models.URLField(
                blank=True, max_length=400, verbose_name="Personal Website"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="topics_i_speak_about",
            field=models.TextField(
                blank=True,
                validators=[django.core.validators.MaxLengthValidator(2000)],
                verbose_name="Topics I Speak About",
            ),
        ),
    ]
