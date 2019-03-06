from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("localgroups", "0003_organisership")]

    operations = [
        migrations.AddField(
            model_name="localgroup",
            name="is_active",
            field=models.BooleanField(default=True),
        )
    ]
