# Generated by Django 2.2.17 on 2021-04-06 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0004_messaginglog"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="first_name",
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name="user",
            name="last_name",
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
