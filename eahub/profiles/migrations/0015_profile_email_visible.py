# Generated by Django 2.2.4 on 2020-03-19 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("profiles", "0014_profile_is_approved")]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="email_visible",
            field=models.BooleanField(default=False),
        )
    ]
