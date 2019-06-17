from django.db import migrations, models

import eahub.profiles.models


class Migration(migrations.Migration):

    dependencies = [("profiles", "0008_profile_slug")]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="name",
            field=models.CharField(
                max_length=200,
                validators=[eahub.profiles.models.validate_sluggable_name],
            ),
        )
    ]
