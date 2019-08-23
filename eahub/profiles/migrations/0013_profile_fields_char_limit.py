import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_profile_links'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cause_areas_other',
            field=models.TextField(blank=True, validators=[django.core.validators.MaxLengthValidator(2000)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='expertise_areas_other',
            field=models.TextField(blank=True, validators=[django.core.validators.MaxLengthValidator(2000)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='summary',
            field=models.TextField(blank=True, validators=[django.core.validators.MaxLengthValidator(2000)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='topics_i_speak_about',
            field=models.TextField(blank=True, validators=[django.core.validators.MaxLengthValidator(2000)]),
        ),
    ]
