from django.db import migrations
from django.db import models
from django.db.models import deletion
from sluggable import fields as sluggable_fields


def create_slugs(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Profile = apps.get_model("profiles", "Profile")
    ProfileSlug = apps.get_model("profiles", "ProfileSlug")
    content_type_for_profile, _ = ContentType.objects.get_or_create(
        app_label="profiles", model="Profile"
    )
    ProfileSlug.objects.bulk_create(
        [
            ProfileSlug(
                content_type=content_type_for_profile,
                object_id=profile.pk,
                slug=profile.slug,
                created=profile.user.date_joined,
            )
            for profile in Profile.objects.select_related("user")
        ]
    )


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("profiles", "0007_profile_is_public"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="slug",
            field=sluggable_fields.SluggableField(unique=True),
        ),
        migrations.CreateModel(
            name="ProfileSlug",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("object_id", models.PositiveIntegerField()),
                (
                    "slug",
                    models.CharField(
                        db_index=True, max_length=255, unique=True, verbose_name="URL"
                    ),
                ),
                (
                    "redirect",
                    models.BooleanField(default=False, verbose_name="Redirection"),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=deletion.PROTECT, to="contenttypes.ContentType"
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.RunPython(code=create_slugs, reverse_code=migrations.RunPython.noop),
    ]
