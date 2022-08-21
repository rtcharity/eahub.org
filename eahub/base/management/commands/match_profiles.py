from typing import List

from django.core.management import base

from eahub.profiles.models import Profile


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        profiles: List[dict] = []
        for profile in Profile.objects.all():
            profiles.append(
                {
                    "is_matchable": profile.get_is_matchable(),   # roland

                    "summary": profile.summary,
                    "offering": profile.offering,
                    "looking_for": profile.looking_for,
                    "cause_areas_other": profile.cause_areas_other,
                    "topics_i_speak_about": profile.topics_i_speak_about,
                    "available_to_volunteer": profile.available_to_volunteer,
                    "open_to_job_offers": profile.open_to_job_offers,
                    "available_as_speaker": profile.available_as_speaker,
                    "is_organiser": profile.is_organiser(),
                    "country": profile.country,
                    "city_or_town": profile.city_or_town,
                    "lat": profile.lat,
                    "lon": profile.lon,
                    "tags_cause_area": profile.get_tags_cause_area_formatted(),
                    "tags_cause_area_pks": profile.tags_cause_area.all().values_list(
                        "id", flat=True
                    ),
                    "tags_organisational_affiliation": profile.get_tags_organisational_affiliation_formatted(),
                    "tags_career_interest": profile.get_tags_career_interest_formatted(),
                    "tags_pledge": profile.get_tags_pledge_formatted(),
                    "local_groups": profile.get_local_groups_formatted(),
                    "organizer_of_local_groups": profile.get_organizer_of_local_groups_formatted(),
                }
            )
