import time

import airtable
from autoslug import utils as autoslug_utils
from django.conf import settings
from django.core.management import base

from ... import models


class Command(base.BaseCommand):
    help = "Imports all local group data from Airtable"

    def handle(self, *args, **options):
        if not settings.LOCAL_GROUPS_AIRTABLE:
            raise base.CommandError("Airtable environment variables are unset")
        local_group_types = {
            "City": models.LocalGroupType.CITY,
            "Country": models.LocalGroupType.COUNTRY,
            "University": models.LocalGroupType.UNIVERSITY,
        }
        local_groups = []
        for table_name, is_active in [("Active", True), ("Inactive", False)]:
            for record in airtable.Airtable(
                table_name=table_name, **settings.LOCAL_GROUPS_AIRTABLE
            ).get_all():
                airtable_fields = record["fields"]
                name = airtable_fields["Group Name"]
                city_or_town = airtable_fields.get("City or Town", "")
                country = airtable_fields.get("Country", "")
                local_group = models.LocalGroup(
                    # This will raise an IntegrityError on collisions
                    slug=autoslug_utils.slugify(name),
                    name=name,
                    is_active=is_active,
                    local_group_type=local_group_types.get(
                        airtable_fields.get("University or City")
                    ),
                    city_or_town=city_or_town,
                    country=country,
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
                if city_or_town and country:
                    self.stdout.write(f"Geocoding: {city_or_town}, {country}")
                    time.sleep(1)
                    local_group.geocode()
                local_groups.append(local_group)
        models.LocalGroup.objects.bulk_create(local_groups)
