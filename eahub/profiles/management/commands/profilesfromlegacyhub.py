import functools
import time

from django.core.management import base
from django import db
from django.db import transaction
from django.utils import html
from django.utils import timezone
from geopy import geocoders

from ... import models
from ....base import models as base_models


CODED_AREAS_BY_LEGACY_NAME = {
    "Coding": models.ExpertiseArea.SOFTWARE_ENGINEERING,
    "Entrepreneurship": models.ExpertiseArea.ENTREPRENEURSHIP,
    "Event planning": models.ExpertiseArea.EVENT_PLANNING,
    "Finance/Investment strategy": models.ExpertiseArea.FINANCE,
    "Graphic design": models.ExpertiseArea.GRAPHIC_DESIGN,
    "Journalism": models.ExpertiseArea.JOURNALISM,
    "Law": models.ExpertiseArea.LAW,
    "Management": models.ExpertiseArea.MANAGEMENT,
    "Marketing/Sales": models.ExpertiseArea.COMMUNICATIONS,
    "Philanthropy": models.ExpertiseArea.PHILANTHROPY_EARNING_TO_GIVE,
    "Public policy/Politics": models.ExpertiseArea.GOVERNMENT_AND_POLICY,
    "Public speaking": models.ExpertiseArea.PUBLIC_SPEAKING,
    "Recruitment": models.ExpertiseArea.RECRUITMENT,
    "Research/Analysis": models.ExpertiseArea.RESEARCH,
    "Statistics/Data science": models.ExpertiseArea.MATH_QUANT_STATS_EXPERTISE,
}


def classify_skills(skills):
    coded_areas = []
    freeform_areas = []
    for skill in skills.split("; "):
        coded_area = CODED_AREAS_BY_LEGACY_NAME.get(skill)
        if coded_area:
            coded_areas.append(coded_area)
        else:
            freeform_areas.append(skill)
        return {
            "expertise_areas": sorted(coded_areas),
            "expertise_areas_other": "; ".join(freeform_areas),
        }


class Command(base.BaseCommand):
    help = "Imports all user profiles from the legacy EA Hub"

    def handle(self, *args, **options):
        if "legacy" not in db.connections:
            raise base.CommandError("LEGACY_DATABASE_URL environment variable is unset")
        with db.connections["legacy"].cursor() as cursor:
            cursor.execute(
                "SELECT "
                "LOWER(users.mail), "
                "IF("
                "users.login, "
                "CONVERT_TZ("
                "FROM_UNIXTIME(users.login), @@SESSION.time_zone, '+00:00'"
                "), "
                "NULL"
                "), "
                "CONVERT_TZ("
                "FROM_UNIXTIME(users.created), @@SESSION.time_zone, '+00:00'"
                "), "
                "TRIM(LEADING 'user/' FROM url_alias.alias), users.name, "
                "IFNULL("
                "field_data_field_in_which_city_do_you_live_."
                "field_in_which_city_do_you_live__value, "
                "''"
                "), "
                "IFNULL("
                "field_data_field_in_which_country_do_you_li."
                "field_in_which_country_do_you_li_value, "
                "''"
                "), "
                "IFNULL(field_data_field_skills.field_skills_value, ''), "
                "IFNULL(field_data_field_more_about_me.field_more_about_me_value, ''), "
                "users.uid "
                "FROM users "
                "LEFT JOIN url_alias ON CONCAT('user/', users.uid) = url_alias.source "
                "LEFT JOIN "
                "("
                "SELECT uid, MIN(pid) AS pid "
                "FROM profile "
                "WHERE type = 'basic_information' "
                "GROUP BY uid"
                ") "
                "AS basic_information "
                "USING (uid) "
                "LEFT JOIN field_data_field_in_which_city_do_you_live_ "
                "ON "
                "basic_information.pid = "
                "field_data_field_in_which_city_do_you_live_.entity_id "
                "AND "
                "field_data_field_in_which_city_do_you_live_.bundle = "
                "'basic_information' "
                "LEFT JOIN field_data_field_in_which_country_do_you_li "
                "ON "
                "basic_information.pid = "
                "field_data_field_in_which_country_do_you_li.entity_id "
                "AND "
                "field_data_field_in_which_country_do_you_li.bundle = "
                "'basic_information' "
                "LEFT JOIN "
                "("
                "SELECT uid, MIN(pid) AS pid "
                "FROM profile "
                "WHERE type = 'your_career' "
                "GROUP BY uid"
                ") "
                "AS your_career "
                "USING (uid) "
                "LEFT JOIN field_data_field_skills "
                "ON your_career.pid = field_data_field_skills.entity_id "
                "LEFT JOIN "
                "("
                "SELECT uid, MIN(pid) AS pid "
                "FROM profile "
                "WHERE type = 'free_text' "
                "GROUP BY uid"
                ") "
                "AS free_text "
                "USING (uid) "
                "LEFT JOIN field_data_field_more_about_me "
                "ON free_text.pid = field_data_field_more_about_me.entity_id "
                "WHERE users.uid AND users.status;"
            )
            rows = cursor.fetchall()

        @functools.lru_cache(maxsize=None)
        def geocode(city_or_town, country):
            if city_or_town and country:
                self.stdout.write(f"Geocoding: {city_or_town}, {country}")
                time.sleep(1)
                location = geocoders.Nominatim(timeout=10).geocode(
                    f"{city_or_town}, {country}"
                )
                if location:
                    return {"lat": location.latitude, "lon": location.longitude}
            return {"lat": None, "lon": None}

        fields = [
            (
                email,
                {
                    "last_login": (
                        last_login
                        and timezone.make_aware(last_login, timezone=timezone.utc)
                    ),
                    "date_joined": timezone.make_aware(
                        date_joined, timezone=timezone.utc
                    ),
                },
                {
                    "slug": slug,
                    "is_public": False,
                    "name": name,
                    "city_or_town": city_or_town,
                    "country": country,
                    "summary": html.strip_tags(summary),
                    "legacy_record": legacy_record,
                    **geocode(city_or_town, country),
                    **classify_skills(skills),
                },
            )
            for (
                email,
                last_login,
                date_joined,
                slug,
                name,
                city_or_town,
                country,
                skills,
                summary,
                legacy_record,
            ) in rows
        ]
        with transaction.atomic():
            for email, user_fields, profile_fields in fields:
                user, user_created = base_models.User.objects.get_or_create(
                    email=email, defaults=user_fields
                )
                if user_created:
                    models.Profile.objects.create(user=user, **profile_fields)
                else:
                    user.date_joined = user_fields["date_joined"]
                    user.save()
                    profile, profile_created = models.Profile.objects.get_or_create(
                        user=user, defaults=profile_fields
                    )
                    if not profile_created:
                        profile.legacy_record = profile_fields["legacy_record"]
                        profile.save()
