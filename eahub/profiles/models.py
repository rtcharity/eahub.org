import io
import json
import pathlib
import shutil
import zipfile

from django import urls
from django.conf import settings
from django.contrib.contenttypes import fields as contenttypes_fields
from django.contrib.postgres import fields as postgres_fields
from django.core import exceptions
from django.db import models
from django_enumfield import enum
from django_upload_path import upload_path
from geopy import geocoders
from sluggable import fields as sluggable_fields
from sluggable import models as sluggable_models
from sluggable import settings as sluggable_settings
from sorl import thumbnail

from ..localgroups.models import LocalGroup


class CauseArea(enum.Enum):

    GLOBAL_POVERTY = 1
    ANIMAL_WELFARE_AND_RIGHTS = 2
    LONG_TERM_FUTURE = 3
    CAUSE_PRIORITISATION = 4
    META = 5
    CLIMATE_CHANGE = 6
    MENTAL_HEALTH = 7
    RATIONALITY = 8

    labels = {
        GLOBAL_POVERTY: "Global poverty",
        ANIMAL_WELFARE_AND_RIGHTS: "Animal welfare/rights",
        LONG_TERM_FUTURE: "Long-term future",
        CAUSE_PRIORITISATION: "Cause prioritisation",
        META: "Meta",
        CLIMATE_CHANGE: "Climate change",
        MENTAL_HEALTH: "Mental health",
        RATIONALITY: "Rationality",
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
    PHILOSOPHY = 12
    HUMANITIES = 13
    PSYCHOLOGY = 14
    PHYSICS = 15
    MEDICINE = 16
    OTHER_SCIENCE = 17
    EVENT_PLANNING = 18
    FINANCE = 19
    GRAPHIC_DESIGN = 20
    JOURNALISM = 21
    LAW = 22
    PHILANTHROPY_EARNING_TO_GIVE = 23
    PUBLIC_SPEAKING = 24
    RECRUITMENT = 25
    EDUCATION = 26

    labels = {
        MANAGEMENT: "Management",
        OPERATIONS: "Operations",
        RESEARCH: "Research",
        GOVERNMENT_AND_POLICY: "Government and policy",
        ENTREPRENEURSHIP: "Entrepreneurship",
        SOFTWARE_ENGINEERING: "Software engineering",
        AI_TECHNICAL_EXPERTISE: "AI technical expertise",
        MATH_QUANT_STATS_EXPERTISE: "Math/quant/stats expertise",
        ECONOMICS_QUANTITATIVE_SOCIAL_SCIENCE: "Economics/quantitative social science",
        MOVEMENT_BUILDING: "Movement building",
        COMMUNICATIONS: "Communications",
        PHILOSOPHY: "Philosophy",
        HUMANITIES: "Humanities",
        PSYCHOLOGY: "Psychology",
        PHYSICS: "Physics",
        MEDICINE: "Medicine",
        OTHER_SCIENCE: "Other science",
        EVENT_PLANNING: "Event planning and logistics",
        FINANCE: "Finance",
        GRAPHIC_DESIGN: "Graphic design",
        JOURNALISM: "Journalism",
        LAW: "Law",
        PHILANTHROPY_EARNING_TO_GIVE: "Philanthropy/earning to give",
        PUBLIC_SPEAKING: "Public speaking",
        RECRUITMENT: "Recruitment",
        EDUCATION: "Education",
    }


class GivingPledge(enum.Enum):

    GIVING_WHAT_WE_CAN = 1
    THE_LIFE_YOU_CAN_SAVE = 2
    ONE_FOR_THE_WORLD = 3
    FOUNDERS_PLEDGE = 4

    labels = {
        GIVING_WHAT_WE_CAN: "Giving What We Can",
        THE_LIFE_YOU_CAN_SAVE: "The Life You Can Save",
        ONE_FOR_THE_WORLD: "One for the World",
        FOUNDERS_PLEDGE: "Founders Pledge",
    }


class OrganisationalAffiliation(enum.Enum):

    EIGHTY_THOUSAND_HOURS = 1
    ANIMAL_CHARITY_EVALUATORS = 2
    BERKELEY_EXISTENTIAL_RISK_INITIATIVE = 3
    CENTER_FOR_APPLIED_RATIONALITY = 4
    CENTER_FOR_HUMAN_COMPATIBLE_AI = 5
    CENTRE_FOR_EFFECTIVE_ALTRUISM = 6
    CSER = 7
    CHARITY_ENTREPRENEURSHIP = 8
    CHARITY_SCIENCE_HEALTH = 9
    FORETHOUGHT_FOUNDATION = 10
    FOUNDATIONAL_RESEARCH_INSTITUTE = 11
    FOUNDERS_PLEDGE = 12
    FUTURE_OF_LIFE_INSTITUTE = 13
    GIVEWELL = 14
    GLOBAL_CATASTROPHIC_RISK_INSTITUTE = 15
    GLOBAL_PRIORITIES_INSTITUTE = 16
    LCFI = 17
    LOCAL_EFFECTIVE_ALTRUISM_NETWORK = 18
    MIRI = 19
    ONE_FOR_THE_WORLD = 20
    OPEN_PHILANTHROPY_PROJECT = 21
    RAISING_FOR_EFFECTIVE_GIVING = 22
    RETHINK_CHARITY = 23
    RETHINK_CHARITY_FORWARD = 24
    RETHINK_PRIORITIES = 25
    SENTIENCE_INSTITUTE = 26
    STIFTUNG_FUR_EFFEKTIVEN_ALTRUISMUS = 27
    STUDENTS_FOR_HIGH_IMPACT_CHARITY = 28
    THE_GOOD_FOOD_INSTITUTE = 29
    THE_LIFE_YOU_CAN_SAVE = 30
    WILD_ANIMAL_INITIATIVE = 31
    ALLFED = 32

    labels = {
        EIGHTY_THOUSAND_HOURS: "80,000 Hours",
        ANIMAL_CHARITY_EVALUATORS: "Animal Charity Evaluators",
        BERKELEY_EXISTENTIAL_RISK_INITIATIVE: "Berkeley Existential Risk Initiative",
        CENTER_FOR_APPLIED_RATIONALITY: "Center for Applied Rationality",
        CENTER_FOR_HUMAN_COMPATIBLE_AI: "Center for Human Compatible AI",
        CENTRE_FOR_EFFECTIVE_ALTRUISM: "Centre for Effective Altruism",
        CSER: "Centre for the Study of Existential Risk",
        CHARITY_ENTREPRENEURSHIP: "Charity Entrepreneurship",
        CHARITY_SCIENCE_HEALTH: "Charity Science Health",
        FORETHOUGHT_FOUNDATION: "Forethought Foundation",
        FOUNDATIONAL_RESEARCH_INSTITUTE: "Foundational Research Institute",
        FOUNDERS_PLEDGE: "Founders Pledge",
        FUTURE_OF_LIFE_INSTITUTE: "Future of Life Institute",
        GIVEWELL: "GiveWell",
        GLOBAL_CATASTROPHIC_RISK_INSTITUTE: "Global Catastrophic Risk Institute",
        GLOBAL_PRIORITIES_INSTITUTE: "Global Priorities Institute",
        LCFI: "Leverhulme Center for the Future of Intelligence",
        LOCAL_EFFECTIVE_ALTRUISM_NETWORK: "Local Effective Altruism Network",
        MIRI: "Machine Intelligence Research Institute",
        ONE_FOR_THE_WORLD: "One for the World",
        OPEN_PHILANTHROPY_PROJECT: "Open Philanthropy Project",
        RAISING_FOR_EFFECTIVE_GIVING: "Raising for Effective Giving",
        RETHINK_CHARITY: "Rethink Charity",
        RETHINK_CHARITY_FORWARD: "Rethink Charity Forward",
        RETHINK_PRIORITIES: "Rethink Priorities",
        SENTIENCE_INSTITUTE: "Sentience Institute",
        STIFTUNG_FUR_EFFEKTIVEN_ALTRUISMUS: "Stiftung für Effektiven Altruismus (EAF)",
        STUDENTS_FOR_HIGH_IMPACT_CHARITY: "Students for High Impact Charity",
        THE_GOOD_FOOD_INSTITUTE: "The Good Food Institute",
        THE_LIFE_YOU_CAN_SAVE: "The Life You Can Save",
        WILD_ANIMAL_INITIATIVE: "Wild Animal Initiative",
        ALLFED: "ALLFED",
    }


def prettify_property_list(property_class, standard_list, other_list):
    pretty_list = ""
    if standard_list:
        pretty_list += ", ".join(map(property_class.label, standard_list))
    if other_list:
        pretty_list = pretty_list + ", " + other_list if standard_list else other_list
    if (standard_list and other_list) is False:
        pretty_list = "N/A"
    return pretty_list


class ProfileSlug(sluggable_models.Slug):
    @classmethod
    def forbidden_slugs(cls):
        return [
            "",
            "delete",
            "download",
            "login",
            "logout",
            "password",
            "profiles",
            "register",
            "signup",
        ]


def slugify_user(name):
    """Generate a slug based on a user's name.

    In particular, don't allow entirely numeric slugs, as those are handled differently.
    """
    slug = sluggable_settings.slugify(name)
    if slug.isdigit():
        return "-" + slug
    return slug


def validate_sluggable_name(name):
    if slugify_user(name) in ProfileSlug.forbidden_slugs():
        raise exceptions.ValidationError(
            'The name "%(name)s" is not allowed', params={"name": name}
        )


class ProfileManager(models.Manager):
    def visible_to_user(self, user):
        if user.is_superuser:
            return self.all()
        return self.filter(models.Q(is_public=True) | models.Q(user_id=user.pk))


class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = sluggable_fields.SluggableField(
        decider=ProfileSlug, populate_from="name", slugify=slugify_user, unique=True
    )
    is_public = models.BooleanField(default=True)
    name = models.CharField(max_length=200, validators=[validate_sluggable_name])
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
    cause_areas_other = models.TextField(blank=True)
    available_to_volunteer = models.BooleanField(null=True, blank=True, default=None)
    open_to_job_offers = models.BooleanField(null=True, blank=True, default=None)
    expertise_areas = postgres_fields.ArrayField(
        enum.EnumField(ExpertiseArea), blank=True, default=list
    )
    expertise_areas_other = models.TextField(blank=True)
    available_as_speaker = models.BooleanField(null=True, blank=True, default=None)
    topics_i_speak_about = models.TextField(blank=True)
    organisational_affiliations = postgres_fields.ArrayField(
        enum.EnumField(OrganisationalAffiliation), blank=True, default=list
    )
    summary = models.TextField(blank=True)
    giving_pledges = postgres_fields.ArrayField(
        enum.EnumField(GivingPledge), blank=True, default=list
    )
    local_groups = models.ManyToManyField(LocalGroup, through="Membership", blank=True)
    legacy_record = models.PositiveIntegerField(
        null=True, default=None, editable=False, unique=True
    )

    slugs = contenttypes_fields.GenericRelation(ProfileSlug)

    objects = ProfileManager()

    class Meta:
        ordering = ["name", "slug"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return urls.reverse("profile", args=[self.slug])

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
        return prettify_property_list(
            CauseArea, self.cause_areas, self.cause_areas_other
        )

    def get_pretty_expertise(self):
        return prettify_property_list(
            ExpertiseArea, self.expertise_areas, self.expertise_areas_other
        )

    def get_pretty_giving_pledges(self):
        if self.giving_pledges:
            return ", ".join(map(GivingPledge.label, self.giving_pledges))
        else:
            return "N/A"

    def get_pretty_organisational_affiliations(self):
        if self.organisational_affiliations:
            return ", ".join(
                map(OrganisationalAffiliation.label, self.organisational_affiliations)
            )
        else:
            return "N/A"

    def get_pretty_local_groups(self):
        if self.local_groups:
            return ", ".join(
                [
                    "{local_group}".format(local_group=x.name)
                    for x in self.local_groups.all()
                ]
            )
        else:
            return "N/A"

    def write_data_export_zip(self, request, response):
        with zipfile.ZipFile(response, mode="w") as zip_file:
            with zip_file.open(
                f"{self.slug}.json", mode="w"
            ) as json_binary_file, io.TextIOWrapper(json_binary_file) as json_file:
                json.dump(
                    {
                        "email": self.user.email,
                        "date_joined": self.user.date_joined.isoformat(),
                        "last_login": self.user.last_login.isoformat(),
                        "url": request.build_absolute_uri(self.get_absolute_url()),
                        "is_public": self.is_public,
                        "name": self.name,
                        "city_or_town": self.city_or_town,
                        "country": self.country,
                        "cause_areas": list(map(CauseArea.label, self.cause_areas)),
                        "cause_areas_other": self.cause_areas_other,
                        "available_to_volunteer": self.available_to_volunteer,
                        "open_to_job_offers": self.open_to_job_offers,
                        "expertise_areas": list(
                            map(ExpertiseArea.label, self.expertise_areas)
                        ),
                        "expertise_areas_other": self.expertise_areas_other,
                        "available_as_speaker": self.available_as_speaker,
                        "topics_i_speak_about": self.topics_i_speak_about,
                        "organisational_affiliations": list(
                            map(
                                OrganisationalAffiliation.label,
                                self.organisational_affiliations,
                            )
                        ),
                        "summary": self.summary,
                        "giving_pledges": list(
                            map(GivingPledge.label, self.giving_pledges)
                        ),
                        "member_of_local_groups": [
                            request.build_absolute_uri(local_group.get_absolute_uri())
                            for local_group in self.local_groups.all()
                        ],
                        "organiser_of_local_groups": [
                            request.build_absolute_uri(local_group.get_absolute_uri())
                            for local_group in self.user.localgroup_set.all()
                        ],
                        "aliases": [
                            request.build_absolute_uri(
                                urls.reverse("profile", kwargs={"slug": slug.slug})
                            )
                            for slug in self.slugs.filter(redirect=True)
                        ],
                        "legacy_hub_url": (
                            self.legacy_record
                            and request.build_absolute_uri(
                                urls.reverse(
                                    "profile_legacy",
                                    kwargs={"legacy_record": self.legacy_record},
                                )
                            )
                        ),
                    },
                    json_file,
                    indent=2,
                )
            if self.image:
                with self.image.open() as image_src_file, zip_file.open(
                    self.slug + pathlib.PurePath(self.image.name).suffix, mode="w"
                ) as image_dst_file:
                    shutil.copyfileobj(image_src_file, image_dst_file)

    def image_placeholder(self):
        return f"Avatar{self.id % 10}.png"

    def has_cause_area_details(self):
        cause_area_details_exist = [
            len(self.cause_areas) > 0,
            len(self.cause_areas_other) > 0,
            len(self.giving_pledges) > 0,
            self.available_to_volunteer,
        ]
        return any(cause_area_details_exist)

    def has_career_details(self):
        career_details_exist = [
            len(self.expertise_areas),
            len(self.expertise_areas_other),
            self.open_to_job_offers,
        ]
        return any(career_details_exist)

    def has_community_details(self):
        community_details_exist = [
            len(self.organisational_affiliations) > 0,
            self.local_groups.exists(),
            self.user.localgroup_set.exists(),
            self.available_as_speaker,
            len(self.topics_i_speak_about) > 0,
        ]
        return any(community_details_exist)


class Membership(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    local_group = models.ForeignKey(LocalGroup, on_delete=models.CASCADE)
