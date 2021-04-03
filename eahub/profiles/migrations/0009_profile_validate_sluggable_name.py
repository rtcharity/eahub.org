from django.db import migrations, models

import eahub.profiles.models
import eahub.profiles.validators


class Migration(migrations.Migration):

    dependencies = [("profiles", "0008_profile_slug")]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="name",
            field=models.CharField(
                max_length=200,
                validators=[eahub.profiles.validators.validate_sluggable_name],
            ),
        )
    ]
