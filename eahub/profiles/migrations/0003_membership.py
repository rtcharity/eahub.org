from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("localgroups", "0003_organisership"),
        ("profiles", "0002_profile_organisational_affiliations"),
    ]

    operations = [
        migrations.CreateModel(
            name="Membership",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "local_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="localgroups.LocalGroup",
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.Profile",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="profile",
            name="local_groups",
            field=models.ManyToManyField(
                blank=True, through="profiles.Membership", to="localgroups.LocalGroup"
            ),
        ),
    ]
