from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("profiles", "0003_membership")]

    operations = [
        migrations.AlterModelOptions(
            name="profile", options={"ordering": ["name", "slug"]}
        )
    ]
