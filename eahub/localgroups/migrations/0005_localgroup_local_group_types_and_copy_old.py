import django.contrib.postgres.fields
import django_enumfield.db.fields
from django.db import migrations

import eahub.localgroups.models


def copy_group_type(apps, schema_editor):
    localgroup = apps.get_model("localgroups", "LocalGroup")
    for row in localgroup.objects.all():
        if row.local_group_type:
            row.local_group_types = [row.local_group_type]
            row.save()


class Migration(migrations.Migration):

    dependencies = [
        ('localgroups', '0004_localgroup_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='localgroup',
            name='local_group_types',
            field=django.contrib.postgres.fields.ArrayField(
                base_field=django_enumfield.db.fields.EnumField(
                    default=1,
                    enum=eahub.localgroups.models.LocalGroupType
                ),
                blank=True,
                default=list,
                size=None
            ),
        ),
        migrations.RunPython(copy_group_type)
    ]
