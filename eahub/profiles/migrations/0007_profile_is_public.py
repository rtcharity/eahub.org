from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("profiles", "0006_profile_legacy_record")]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="is_public",
            field=models.BooleanField(default=True),
        )
    ]
