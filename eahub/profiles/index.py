from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from eahub.profiles.models import Profile


@register(Profile)
class ProfileIndex(AlgoliaIndex):
    index_name = 'profiles'
    should_index = 'is_searchable'
    
    fields = [
        "name",
        ["get_email_searchable", "email"],
        "summary",
        "topics_i_speak_about",
        "expertise_areas_other",
        "cause_areas_other",

        ["get_absolute_url", "url"],
        "image",
        "personal_website_url",
        "facebook_url",
        "linkedin_url",

        "available_as_speaker",
        "available_to_volunteer",
        "open_to_job_offers",

        "city_or_town",
        "country",
        "lon",
        "lat",

        ["get_cause_areas_searchable", "cause_areas"],
        ["get_expertise_searchable", "expertise"],
        ["get_career_interest_areas_searchable", "career_interest_areas"],
        ["get_giving_pledges_searchable", "giving_pledges"],
    ]
