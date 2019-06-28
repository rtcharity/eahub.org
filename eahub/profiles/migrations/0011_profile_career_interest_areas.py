from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("profiles", "0010_remove_profile_subscribed_to_email_updates")]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="career_interest_areas",
            field=models.TextField(blank=True),
        )
    ]
