from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from django.conf import settings

from eahub.profiles.models import Profile, ProfileTag

if settings.IS_ENABLE_ALGOLIA:

    @register(Profile)
    class ProfileIndex(AlgoliaIndex):
        index_name = settings.ALGOLIA["INDEX_NAME_PROFILES"]
        should_index = "is_searchable"

        fields = [
            "job_title",
            ["get_full_name", "name"],
            ["get_messaging_url_if_can_receive_message", "messaging_url"],
            "summary",
            ["get_tags_speech_topic_formatted", "speech_topics"],
            "topics_i_speak_about",
            "expertise_areas_other",
            "cause_areas_other",
            ["get_absolute_url", "url"],
            ["get_image_url", "image"],
            "personal_website_url",
            "facebook_url",
            "linkedin_url",
            "available_as_speaker",
            "available_to_volunteer",
            "open_to_job_offers",
            "is_organiser",
            "city_or_town",
            "country",
            "lon",
            "lat",
            ["get_tags_generic_formatted", "tags"],
            ["get_tags_cause_area_formatted", "cause_areas"],
            ["get_tags_expertise_formatted", "expertise"],
            ["get_tags_career_interest_formatted", "career_interest_areas"],
            ["get_tags_pledge_formatted", "giving_pledges"],
            ["get_tags_event_attended_formatted", "events_attended"],
            [
                "get_tags_organisational_affiliation_formatted",
                "organisational_affiliations",
            ],
            ["get_local_groups_formatted", "local_groups"],
            ["get_organizer_of_local_groups_formatted", "organizer_of_local_groups"],
            ["offering", "offering"],
            ["looking_for", "looking_for"],
        ]

    @register(ProfileTag)
    class ProfileTagIndex(AlgoliaIndex):
        index_name = settings.ALGOLIA["INDEX_NAME_TAGS"]
        fields = [
            "name",
            "description",
            "synonyms",
            ["get_types_formatted", "types"],
            "created_at",
            "status",
            "is_featured",
            "count",
        ]
