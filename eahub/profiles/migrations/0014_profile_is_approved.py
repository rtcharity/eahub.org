from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("profiles", "0013_profile_fields_char_limit")]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="is_approved",
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="profile",
            name="is_approved",
            field=models.BooleanField(default=False),
        ),
    ]
