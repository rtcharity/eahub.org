from django.contrib.postgres import operations
from django.contrib.postgres.fields import citext
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("profiles", "0020_delete_duplicate_email_profiles")]

    operations = [
        operations.CITextExtension(),
        migrations.AlterField(
            model_name="profile",
            name="email",
            field=citext.CIEmailField(max_length=254, unique=True),
        ),
    ]
