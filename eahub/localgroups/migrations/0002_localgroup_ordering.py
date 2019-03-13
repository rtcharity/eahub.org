from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("localgroups", "0001_initial")]

    operations = [
        migrations.AlterModelOptions(
            name="localgroup", options={"ordering": ["name", "slug"]}
        )
    ]
