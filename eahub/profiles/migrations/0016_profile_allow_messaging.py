# Generated by Django 2.2.16 on 2021-01-24 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("profiles", "0015_profile_email_visible")]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="allow_messaging",
            field=models.BooleanField(default=False),
        )
    ]
