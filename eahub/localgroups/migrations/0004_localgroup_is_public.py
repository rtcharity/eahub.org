from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("localgroups", "0003_localgroup_last_edited")]

    operations = [
        migrations.AddField(
            model_name="localgroup",
            name="is_public",
            field=models.BooleanField(default=True),
        )
    ]
