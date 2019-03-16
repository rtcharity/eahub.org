from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("profiles", "0005_other_fields")]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="legacy_record",
            field=models.PositiveIntegerField(
                default=None, editable=False, null=True, unique=True
            ),
        )
    ]
