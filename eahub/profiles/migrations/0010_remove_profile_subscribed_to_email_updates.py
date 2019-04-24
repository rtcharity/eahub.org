from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("profiles", "0009_profile_validate_sluggable_name")]

    operations = [
        migrations.RemoveField(model_name="profile", name="subscribed_to_email_updates")
    ]
