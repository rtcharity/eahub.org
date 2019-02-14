from django.contrib.postgres import operations
from django.contrib.postgres.fields import citext
from django.db import migrations
from django.db import models
from django.db.models import functions


def delete_duplicate_email_profiles(apps, schema_editor):
    Profile = apps.get_model("profiles", "Profile")
    Profile.objects.exclude(
        id=models.Subquery(
            Profile.objects.annotate(normalized_email=functions.Lower("email"))
            .filter(normalized_email=functions.Lower(models.OuterRef("email")))
            .values(canonical_id=models.Min("id"))
        )
    ).delete()


class Migration(migrations.Migration):

    dependencies = [("profiles", "0019_auto_20190206_0632")]

    operations = [
        operations.CITextExtension(),
        migrations.RunPython(
            delete_duplicate_email_profiles, hints={"model_name": "profile"}
        ),
        migrations.AlterField(
            model_name="profile",
            name="email",
            field=citext.CIEmailField(max_length=254, unique=True),
        ),
    ]
