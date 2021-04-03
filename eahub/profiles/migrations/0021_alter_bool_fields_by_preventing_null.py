from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0020_alter_bool_fields_by_removing_null"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="available_as_speaker",
            field=models.BooleanField(
                blank=True,
                null=False,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="available_to_volunteer",
            field=models.BooleanField(
                blank=True,
                null=False,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="open_to_job_offers",
            field=models.BooleanField(
                blank=True,
                null=False,
            ),
        ),
    ]
