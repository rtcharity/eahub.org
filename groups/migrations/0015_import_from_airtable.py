import itertools
import time

import airtable
from django.conf import settings
from django.db import migrations
from geopy import geocoders


def import_from_airtable(apps, schema_editor):
    if not settings.LOCAL_GROUPS_AIRTABLE:
        return
    Group = apps.get_model("groups", "Group")
    group_type_choices = {
        display_name: db_name
        for db_name, display_name in Group._meta.get_field("group_type").choices
    }
    group_type_choices[None] = None
    geolocator = geocoders.Nominatim(timeout=10)
    local_groups = []
    for local_group_airtable_record in itertools.chain.from_iterable(
        airtable.Airtable(
            table_name="Active", **settings.LOCAL_GROUPS_AIRTABLE
        ).get_iter()
    ):
        airtable_fields = local_group_airtable_record["fields"]
        group_type = airtable_fields.get("University or City")
        city_or_town = airtable_fields.get("City or Town")
        country = airtable_fields.get("Country")
        if city_or_town and country:
            location = geolocator.geocode(f"{city_or_town}, {country}")
            time.sleep(1)
        else:
            location = None
        local_groups.append(
            Group(
                name=airtable_fields["Group Name"],
                group_type=group_type_choices.get(group_type, "OTHER"),
                group_type_other=(
                    None if group_type in group_type_choices else group_type
                ),
                city_or_town=city_or_town,
                country=country,
                website=airtable_fields.get("Website"),
                facebook_group=airtable_fields.get("Facebook Group"),
                facebook_page=airtable_fields.get("Facebook Page"),
                email=airtable_fields.get(
                    "Official Group Email", airtable_fields.get("LEAN email")
                ),
                meetup_url=airtable_fields.get("Meetup.com"),
                lat=location and (location.latitude or None),
                lon=location and (location.longitude or None),
                airtable_record=local_group_airtable_record["id"],
            )
        )
    Group.objects.bulk_create(local_groups)


def delete_from_airtable(apps, schema_editor):
    Group = apps.get_model("groups", "Group")
    Group.objects.filter(airtable_record__isnull=False).delete()


class Migration(migrations.Migration):

    dependencies = [("groups", "0014_group_airtable_record")]

    operations = [
        migrations.RunPython(
            code=import_from_airtable, reverse_code=delete_from_airtable
        )
    ]
