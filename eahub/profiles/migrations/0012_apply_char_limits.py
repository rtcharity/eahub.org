from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("profiles", "0011_profile_career_interest_areas")]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="cause_areas_other",
            field=models.TextField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name="profile",
            name="expertise_areas_other",
            field=models.TextField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name="profile",
            name="summary",
            field=models.TextField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name="profile",
            name="topics_i_speak_about",
            field=models.TextField(blank=True, max_length=2000),
        ),
    ]
