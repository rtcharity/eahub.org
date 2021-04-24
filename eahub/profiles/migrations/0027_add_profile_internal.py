import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0026_add_visibility"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProfileInternal",
            fields=[
                (
                    "profile_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="profiles.Profile",
                    ),
                ),
            ],
            bases=("profiles.profile",),
        )
    ]
