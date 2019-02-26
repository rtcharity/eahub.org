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
    organisational_affiliation = models.TextField(blank=True)
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
                ["summary", self.summary],
                ["giving_pledges", self.get_pretty_giving_pledges()],
            ]
        )
        return response

    def image_placeholder(self):
        return f"Avatar{self.id % 10}.png"
