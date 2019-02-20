import logging
import time

import airtable
from django.conf import settings
from django.db import migrations
from django.template import defaultfilters
from geopy import geocoders

from .. import models


logger = logging.getLogger(__name__)


def import_from_airtable(apps, schema_editor):
    if not settings.LOCAL_GROUPS_AIRTABLE:
        return
    LocalGroup = apps.get_model("localgroups", "LocalGroup")
    local_group_types = {
        "City": models.LocalGroupType.CITY,
        "Country": models.LocalGroupType.COUNTRY,
        "University": models.LocalGroupType.UNIVERSITY,
    }
    geolocator = geocoders.Nominatim(timeout=10)
    local_groups = []
    for record in airtable.Airtable(
        table_name="Active", **settings.LOCAL_GROUPS_AIRTABLE
    ).get_all():
        airtable_fields = record["fields"]
        name = airtable_fields["Group Name"]
        city_or_town = airtable_fields.get("City or Town")
        country = airtable_fields.get("Country")
        if city_or_town and country:
            logger.info("Geocoding: %s, %s", city_or_town, country)
            location = geolocator.geocode(f"{city_or_town}, {country}")
            time.sleep(1)
        else:
            location = None
        local_groups.append(
            LocalGroup(
                # This will raise an IntegrityError on collisions
                slug=defaultfilters.slugify(name),
                name=name,
                local_group_type=local_group_types.get(
                    airtable_fields.get("University or City")
                ),
                city_or_town=city_or_town or "",
                country=country or "",
                lat=location and (location.latitude or None),
                lon=location and (location.longitude or None),
                website=airtable_fields.get("Website", ""),
                facebook_group=airtable_fields.get("Facebook Group", ""),
                facebook_page=airtable_fields.get("Facebook Page", ""),
                email=airtable_fields.get(
                    "Official Group Email",
                    airtable_fields.get(
                        "LEAN email", airtable_fields.get("EAF email", "")
                    ),
                ),
                meetup_url=airtable_fields.get("Meetup.com", ""),
                airtable_record=record["id"],
            )
        )
    LocalGroup.objects.bulk_create(local_groups)


def delete_from_airtable(apps, schema_editor):
    LocalGroup = apps.get_model("localgroups", "LocalGroup")
    LocalGroup.objects.filter(airtable_record__isnull=False).delete()


class Migration(migrations.Migration):
    dependencies = [("localgroups", "0001_initial")]
    operations = [
        migrations.RunPython(
            code=import_from_airtable, reverse_code=delete_from_airtable
        )
    ]
