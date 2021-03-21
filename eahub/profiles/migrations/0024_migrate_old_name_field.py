from django.db import migrations


def transform_field_name_to_first_name(apps, schema_editor):
    Profile = apps.get_model("profiles", "Profile")
    for profile in Profile.objects.all():
        is_already_has_last_name = profile.last_name == ""
        if is_already_has_last_name:
            *first_name_list, last_name = profile.first_name.split()
            if first_name_list:
                profile.first_name = " ".join(first_name_list)
                profile.last_name = last_name
            else:
                profile.first_name = last_name
            profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0023_add_fields_from_EAG"),
    ]

    operations = [
        migrations.RunPython(
            code=transform_field_name_to_first_name,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
