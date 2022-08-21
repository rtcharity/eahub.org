# Generated by Django 2.2.26 on 2022-07-17 18:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0030_profile_opt_in_to_matchmaking'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='number_of_matchmaking_introductions_per_period',
            field=models.IntegerField(blank=1, default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Up to how many times per month are you willing to be matched?'),
        ),
    ]
