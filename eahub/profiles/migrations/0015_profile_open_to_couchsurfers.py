from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("profiles", "0014_profile_is_approved")]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="open_to_couchsurfers",
            field=models.BooleanField(default=False),
        )
    ]
