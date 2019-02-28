import csv

import autoslug
from django.conf import settings
from django.contrib.postgres import fields as postgres_fields
from django.db import models
from django_enumfield import enum
from django_upload_path import upload_path
from geopy import geocoders
from sorl import thumbnail


class CauseArea(enum.Enum):

    GLOBAL_POVERTY = 1
    ANIMAL_WELFARE_AND_RIGHTS = 2
    LONG_TERM_FUTURE = 3
    CAUSE_PRIORITISATION = 4
    META = 5

    labels = {
        GLOBAL_POVERTY: "Global Poverty",
        ANIMAL_WELFARE_AND_RIGHTS: "Animal Welfare/Rights",
        LONG_TERM_FUTURE: "Long-term Future",
        CAUSE_PRIORITISATION: "Cause Prioritisation",
        META: "Meta",
    }


class ExpertiseArea(enum.Enum):

    MANAGEMENT = 1
    OPERATIONS = 2
    RESEARCH = 3
    GOVERNMENT_AND_POLICY = 4
    ENTREPRENEURSHIP = 5
    SOFTWARE_ENGINEERING = 6
    AI_TECHNICAL_EXPERTISE = 7
    MATH_QUANT_STATS_EXPERTISE = 8
    ECONOMICS_QUANTITATIVE_SOCIAL_SCIENCE = 9
    MOVEMENT_BUILDING = 10
    COMMUNICATIONS = 11

    labels = {
        MANAGEMENT: "Management",
        OPERATIONS: "Operations",
        RESEARCH: "Research",
        GOVERNMENT_AND_POLICY: "Government and policy",
        ENTREPRENEURSHIP: "Entrepreneurship",
        SOFTWARE_ENGINEERING: "Software engineering",
        AI_TECHNICAL_EXPERTISE: "AI technical expertise",
        MATH_QUANT_STATS_EXPERTISE: "Math, quant, stats expertise",
        ECONOMICS_QUANTITATIVE_SOCIAL_SCIENCE: "Economics, quantitative social science",
        MOVEMENT_BUILDING: "Movement building",
        COMMUNICATIONS: "Communications",
    }


class GivingPledge(enum.Enum):

    GIVING_WHAT_WE_CAN = 1
    THE_LIFE_YOU_CAN_SAVE = 2
    ONE_FOR_THE_WORLD = 3

    labels = {
        GIVING_WHAT_WE_CAN: "Giving What We Can",
        THE_LIFE_YOU_CAN_SAVE: "The Life You Can Save",
        ONE_FOR_THE_WORLD: "One for the World",
    }

class OrganisationalAffiliation(enum.Enum):

    EIGHTY_THOUSAND_HOURS = 1
    ANIMAL_CHARITY_EVALUATORS = 2
    BERKELEY_EXISTENTIAL_RISK_INITIATIVE = 3
    CENTER_FOR_HUMAN_COMPATIBLE_AI = 4
    CENTRE_FOR_EFFECTIVE_ALTRUISM = 5
    CENTER_FOR_APPLIED_RATIONALITY = 6
    CENTRE_FOR_THE_STUDY_OF_EXISTENTIAL_RISK = 7
    CHARITY_ENTREPRENEURSHIP = 8
    CHARITY_SCIENCE_HEALTH = 9
    FORETHOUGHT_FOUNDATION = 10
    FOUNDATIONAL_RESEARCH_INSTITUTE = 11
    FOUNDERS_PLEDGE = 12
    FUTURE_OF_LIFE_INSTITUTE = 13
    GIVEWELL = 14
    GLOBAL_CATASTROPHIC_RISK_INSTITUTE = 15
    GLOBAL_PRIORITIES_INSTITUTE = 16
    LEVERHULME_CENTER_FOR_THE_FUTURE_OF_INTELLIGENCE = 17
    LOCAL_EFFECTIVE_ALTRUISM_NETWORK = 18
    MACHINE_INTELLIGENCE_RESEARCH_INSTITUTE = 19
    ONE_FOR_THE_WORLD = 20
    OPEN_PHILANTHROPY_PROJECT = 21
    RAISING_FOR_EFFECTIVE_GIVING = 22
    RETHINK_CHARITY = 23
    RETHINK_CHARITY_FORWARD = 24
    RETHINK_PRIORITIES = 25
    SENTIENCE_INSTITUTE = 26
    STUDENTS_FOR_HIGH_IMPACT_CHARITY = 27
    STIFTUNG_FUR_EFFEKTIVEN_ALTRUISMUS = 28
    THE_GOOD_FOOD_INSTITUTE = 29
    THE_LIFE_YOU_CAN_SAVE = 30
    WILD_ANIMAL_INITIATIVE = 31

    labels = {
        EIGHTY_THOUSAND_HOURS: "80,000 Hours",
        ANIMAL_CHARITY_EVALUATORS: "Animal Charity Evaluators",
        BERKELEY_EXISTENTIAL_RISK_INITIATIVE: "Berkeley Existential Risk Initiative",
        CENTER_FOR_HUMAN_COMPATIBLE_AI: "Center for Human Compatible AI",
        CENTRE_FOR_EFFECTIVE_ALTRUISM: "Centre for Effective Altruism",
        CENTER_FOR_APPLIED_RATIONALITY: "Center for Applied Rationality",
        CENTRE_FOR_THE_STUDY_OF_EXISTENTIAL_RISK: "Centre for the Study of Existential Risk",
        CHARITY_ENTREPRENEURSHIP: "Charity Entrepreneurship",
        CHARITY_SCIENCE_HEALTH: "Charity Science Health",
        FORETHOUGHT_FOUNDATION: "Forethought Foundation",
        FOUNDATIONAL_RESEARCH_INSTITUTE: "Foundational Research Institute",
        FOUNDERS_PLEDGE: "Founders Pledge",
        FUTURE_OF_LIFE_INSTITUTE: "Future of Life Institute",
        GIVEWELL: "GiveWell",
        GLOBAL_CATASTROPHIC_RISK_INSTITUTE: "Global Catastrophic Risk Institute",
        GLOBAL_PRIORITIES_INSTITUTE: "Global Priorities Institute",
        LEVERHULME_CENTER_FOR_THE_FUTURE_OF_INTELLIGENCE: "Leverhulme Center for the Future of Intelligence",
        LOCAL_EFFECTIVE_ALTRUISM_NETWORK: "Local Effective Altruism Network",
        MACHINE_INTELLIGENCE_RESEARCH_INSTITUTE: "Machine Intelligence Research Institute",
        ONE_FOR_THE_WORLD: "One for the World",
        OPEN_PHILANTHROPY_PROJECT: "Open Philanthropy Project",
        RAISING_FOR_EFFECTIVE_GIVING: "Raising for Effective Giving",
        RETHINK_CHARITY: "Rethink Charity",
        RETHINK_CHARITY_FORWARD: "Rethink Charity Forward",
        RETHINK_PRIORITIES: "Rethink Priorities",
        STUDENTS_FOR_HIGH_IMPACT_CHARITY: "Students for High Impact Charity",
        SENTIENCE_INSTITUTE: "Sentience Institute",
        STIFTUNG_FUR_EFFEKTIVEN_ALTRUISMUS: "Stiftung für Effektiven Altruismus (EAF)",
        THE_GOOD_FOOD_INSTITUTE: "The Good Food Institute",
        THE_LIFE_YOU_CAN_SAVE: "The Life You Can Save",
        WILD_ANIMAL_INITIATIVE: "Wild Animal Initiative"
    }


class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = autoslug.AutoSlugField(populate_from="name", unique=True)
    name = models.CharField(max_length=200)
    image = thumbnail.ImageField(
        upload_to=upload_path.auto_cleaned_path_stripped_uuid4, blank=True
    )
    city_or_town = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    lat = models.FloatField(null=True, blank=True, default=None)
    lon = models.FloatField(null=True, blank=True, default=None)
    cause_areas = postgres_fields.ArrayField(
        enum.EnumField(CauseArea), blank=True, default=list
    )
    available_to_volunteer = models.BooleanField(null=True, blank=True, default=None)
    open_to_job_offers = models.BooleanField(null=True, blank=True, default=None)
    expertise_areas = postgres_fields.ArrayField(
        enum.EnumField(ExpertiseArea), blank=True, default=list
    )
    available_as_speaker = models.BooleanField(null=True, blank=True, default=None)
    organisational_affiliations = postgres_fields.ArrayField(
        enum.EnumField(OrganisationalAffiliation), blank=True, default=list
    )
    summary = models.TextField(blank=True)
    giving_pledges = postgres_fields.ArrayField(
        enum.EnumField(GivingPledge), blank=True, default=list
    )
    subscribed_to_email_updates = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def geocode(self):
        self.lat = None
        self.lon = None
        if self.city_or_town and self.country:
            location = geocoders.Nominatim(timeout=10).geocode(
                f"{self.city_or_town}, {self.country}"
            )
            if location:
                self.lat = location.latitude
                self.lon = location.longitude
        return self

    def get_pretty_cause_areas(self):
        if self.cause_areas:
            return ", ".join(map(CauseArea.label, self.cause_areas))
        else:
            return "N/A"

    def get_pretty_expertise(self):
        if self.expertise_areas:
            return ", ".join(map(ExpertiseArea.label, self.expertise_areas))
        else:
            return "N/A"

    def get_pretty_giving_pledges(self):
        if self.giving_pledges:
            return ", ".join(map(GivingPledge.label, self.giving_pledges))
        else:
            return "N/A"

    def get_pretty_organisational_affiliations(self):
        if self.organisational_affiliations:
            return ", ".join(map(OrganisationalAffiliation.label, self.organisational_affiliations))
        else:
            return "N/A"

    def csv(self, response):
        writer = csv.writer(response)
        writer.writerows(
            [
                ["url", f"https://eahub.org/profile/{self.slug}"],
                ["email", self.user.email],
                ["name", self.name],
                ["city_or_town", self.city_or_town],
                ["country", self.country],
                ["cause_areas", self.get_pretty_cause_areas()],
                ["available_to_volunteer", self.available_to_volunteer],
                ["open_to_job_offers", self.open_to_job_offers],
                ["expertise_areas", self.get_pretty_expertise()],
                ["available_as_speaker", self.available_as_speaker],
                ["organisational_affiliations", self.get_pretty_organisational_affiliations()],
                ["summary", self.summary],
                ["giving_pledges", self.get_pretty_giving_pledges()],
            ]
        )
        return response

    def image_placeholder(self):
        return f"Avatar{self.id % 10}.png"
