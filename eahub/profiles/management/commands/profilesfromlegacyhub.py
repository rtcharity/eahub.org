import functools
import time

from django import db
from django.core.management import base
from django.db import transaction
from django.utils import html, timezone
from geopy import geocoders

from ....base import models as base_models
from ... import models


def collect_cause_areas(
    global_poverty,
    animal_welfare_and_rights,
    long_term_future,
    cause_prioritisation,
    meta,
    climate_change,
):
    cause_areas = []
    if global_poverty:
        cause_areas.append(models.CauseArea.GLOBAL_POVERTY)
    if animal_welfare_and_rights:
        cause_areas.append(models.CauseArea.ANIMAL_WELFARE_AND_RIGHTS)
    if long_term_future:
        cause_areas.append(models.CauseArea.LONG_TERM_FUTURE)
    if cause_prioritisation:
        cause_areas.append(models.CauseArea.CAUSE_PRIORITISATION)
    if meta:
        cause_areas.append(models.CauseArea.META)
    if climate_change:
        cause_areas.append(models.CauseArea.CLIMATE_CHANGE)
    return cause_areas


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
                "IFNULL(cause_areas.global_poverty, FALSE), "
                "IFNULL(cause_areas.animal_welfare_and_rights, FALSE), "
                "IFNULL(cause_areas.long_term_future, FALSE), "
                "IFNULL(cause_areas.cause_prioritisation, FALSE), "
                "IFNULL(cause_areas.meta, FALSE), "
                "IFNULL(cause_areas.climate_change, FALSE), "
                "IFNULL(cause_areas.cause_areas_other, ''), "
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
                "WHERE type = 'your_views_and_values' "
                "GROUP BY uid"
                ") "
                "AS your_views_and_values "
                "USING (uid) "
                "LEFT JOIN "
                "("
                "SELECT "
                "entity_id, "
                "MAX(coded_cause_area = 1) AS global_poverty, "
                "MAX(coded_cause_area = 2) AS animal_welfare_and_rights, "
                "MAX(coded_cause_area = 3) AS long_term_future, "
                "MAX(coded_cause_area = 4) AS cause_prioritisation, "
                "MAX(coded_cause_area = 5) AS meta, "
                "MAX(coded_cause_area = 6) AS climate_change, "
                "GROUP_CONCAT("
                "IF("
                "coded_cause_area IS NULL, "
                "field_interest_in_causes_and_com_value, "
                "NULL"
                ") "
                "ORDER BY delta "
                "SEPARATOR '; '"
                ") "
                "AS cause_areas_other "
                "FROM "
                "("
                "SELECT "
                "entity_id, "
                "delta, "
                "field_interest_in_causes_and_com_value, "
                "CASE field_interest_in_causes_and_com_value "
                "WHEN 'Earn-to-give' THEN 0 "
                "WHEN 'Entrepreneurship' THEN 0 "
                "WHEN 'Global poverty' THEN 1 "
                "WHEN 'Animal welfare' THEN 2 "
                "WHEN 'Existential risk / far future outcomes' THEN 3 "
                "WHEN 'Existential risk and far future causes' THEN 3 "
                "WHEN 'Machine intelligence risk' THEN 3 "
                "WHEN 'Molecular nanotechnology' THEN 3 "
                "WHEN 'Nuclear technology' THEN 3 "
                "WHEN 'Synthetic biology risk' THEN 3 "
                "WHEN 'Effective giving' THEN 4 "
                "WHEN 'Prioritization research' THEN 4 "
                "WHEN 'Movement-building' THEN 5 "
                "WHEN 'Rationality' THEN 5 "
                "WHEN 'Climate change' THEN 6 "
                "ELSE NULL "
                "END "
                "AS coded_cause_area "
                "FROM field_data_field_interest_in_causes_and_com"
                ") "
                "AS coded_cause_areas "
                "GROUP BY entity_id"
                ") "
                "AS cause_areas "
                "ON your_views_and_values.pid = cause_areas.entity_id "
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
                "WHERE "
                "users.uid "
                "AND users.status "
                "AND NOT EXISTS "
                "("
                "SELECT NULL "
                "FROM redirect "
                "WHERE "
                "redirect.source = url_alias.alias "
                "AND redirect.redirect != CONCAT('user/', users.uid)"
                ");"
            )
            profile_rows = cursor.fetchall()
            cursor.execute(
                "SELECT users.uid, TRIM(LEADING 'user/' FROM redirect.source) "
                "FROM "
                "redirect "
                "INNER JOIN users ON redirect.redirect = CONCAT('user/', users.uid) "
                "WHERE "
                "redirect.source LIKE 'user/%' "
                "AND redirect.status "
                "AND users.uid "
                "AND users.status;"
            )
            redirect_rows = list(cursor.fetchall())

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
                    "cause_areas": collect_cause_areas(
                        global_poverty,
                        animal_welfare_and_rights,
                        long_term_future,
                        cause_prioritisation,
                        meta,
                        climate_change,
                    ),
                    "cause_areas_other": cause_areas_other,
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
                global_poverty,
                animal_welfare_and_rights,
                long_term_future,
                cause_prioritisation,
                meta,
                climate_change,
                cause_areas_other,
                skills,
                summary,
                legacy_record,
            ) in profile_rows
        ]
        with transaction.atomic():
            profiles_by_legacy_record = {}
            created_by_legacy_record = {}
            for email, user_fields, profile_fields in fields:
                user, user_created = base_models.User.objects.get_or_create(
                    email=email, defaults=user_fields
                )
                if user_created:
                    profile = models.Profile.objects.create(user=user, **profile_fields)
                else:
                    user.date_joined = user_fields["date_joined"]
                    user.save()
                    profile, profile_created = models.Profile.objects.get_or_create(
                        user=user, defaults=profile_fields
                    )
                    if not profile_created:
                        profile.legacy_record = profile_fields["legacy_record"]
                        profile.save()
                        slug = profile_fields["slug"]
                        if profile.slug != slug:
                            redirect_rows.append((profile.legacy_record, slug))
                profiles_by_legacy_record[profile.legacy_record] = profile
                created_by_legacy_record[profile.legacy_record] = user.date_joined
            models.ProfileSlug.objects.bulk_create(
                [
                    models.ProfileSlug(
                        content_object=profiles_by_legacy_record[legacy_record],
                        slug=slug,
                        redirect=True,
                        created=created_by_legacy_record[legacy_record],
                    )
                    for legacy_record, slug in redirect_rows
                    if legacy_record in profiles_by_legacy_record
                    and profiles_by_legacy_record[legacy_record].slug != slug
                ]
            )
