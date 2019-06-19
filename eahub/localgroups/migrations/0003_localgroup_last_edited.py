from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("localgroups", "0002_localgroup_ordering")]

    operations = [
        migrations.AddField(
            model_name="localgroup",
            name="last_edited",
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name="localgroup",
            name="last_edited",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
