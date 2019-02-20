from django.conf import settings
from django.contrib.auth import base_user
from django.db import migrations


def admin_emails():
    return (email.lower() for _, email in settings.ADMINS)


def create_superusers(apps, schema_editor):
    User = apps.get_model("base", "User")
    User.objects.bulk_create(
        [
            User(email=email, is_superuser=True, is_staff=True)
            for email in admin_emails()
        ]
    )


def delete_superusers(apps, schema_editor):
    User = apps.get_model("base", "User")
    User.objects.filter(email__in=admin_emails()).delete()


class Migration(migrations.Migration):
    dependencies = [("base", "0001_initial")]
    operations = [
        migrations.RunPython(code=create_superusers, reverse_code=delete_superusers)
    ]
