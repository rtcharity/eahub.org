from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("localgroups", "0002_import_from_airtable"),
    ]

    operations = [
        migrations.CreateModel(
            name="Organisership",
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
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="localgroup",
            name="organisers",
            field=models.ManyToManyField(
                blank=True,
                through="localgroups.Organisership",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
