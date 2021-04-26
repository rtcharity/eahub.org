import uuid
from typing import List, Optional

from django import urls
from django.conf import settings
from django.contrib.contenttypes import fields as contenttypes_fields
from django.contrib.postgres import fields as postgres_fields
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils import timezone
from django_enumfield import enum
from django_upload_path import upload_path
from enumfields import Enum, EnumField
from geopy import geocoders
from sluggable import fields as sluggable_fields
from sluggable import models as sluggable_models
from sluggable import settings as sluggable_settings
from sorl import thumbnail
from sorl.thumbnail import get_thumbnail

from eahub.localgroups.models import LocalGroup
from eahub.profiles.legacy import (
    CauseArea,
    ExpertiseArea,
    GivingPledge,
    OrganisationalAffiliation,
)
from eahub.profiles.validators import validate_sluggable_name


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
    slug = sluggable_settings.slugify(name)
    is_fully_numeric_and_needs_adjustments = slug.isdigit()
    if is_fully_numeric_and_needs_adjustments:
        return "-" + slug
    return slug


class VisibilityEnum(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    PRIVATE = "private"

    class Labels:
        PUBLIC = "Public (visible to anyone on the web)"
        INTERNAL = "Internal (visible to approved Hub users)"
        PRIVATE = "Private (visible to you only)"


class ProfileTagTypeEnum(Enum):
    GENERIC = "generic"
    AFFILIATION = "affiliation"
    EXPERTISE_AREA = "expertise_area"
    CAUSE_AREA = "cause_area"
    CAUSE_AREA_EXPERTISE = "cause_area_expertise"
    ORGANISATIONAL_AFFILIATION = "organisational_affiliation"
    CAREER_INTEREST = "career_interest"
    SPEECH_TOPIC = "speech_topic"
    PLEDGE = "pledge"
    UNIVERSITY = "university"
    EVENT_ATTENDED = "event_attended"
    CAREER_STAGE = "career_stage"
    EA_INVOLVEMENT = "ea_involvement"


class ProfileTagType(models.Model):
    type = EnumField(ProfileTagTypeEnum, max_length=128, unique=True)

    def __str__(self):
        return str(self.type)


class ProfileTagStatus(Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING = "pending"


class ProfileTag(models.Model):
    name = models.CharField(max_length=128, unique=True)
    types = models.ManyToManyField(ProfileTagType)
    author = models.ForeignKey(
        "profiles.Profile", on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.TextField(blank=True)
    synonyms = models.CharField(blank=True, max_length=1024)
    status = EnumField(
        ProfileTagStatus, default=ProfileTagStatus.APPROVED, max_length=64
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_types_formatted(self) -> List[str]:
        return [type_instance.type.value for type_instance in self.types.all()]

    def count(self) -> int:
        count = 0
        for enum_member in ProfileTagTypeEnum:
            lookup_name = f"tags_{enum_member.value}__in"
            count += Profile.objects.filter(**{lookup_name: [self]}).count()
        return count

    def __str__(self):
        return self.name


class ProfileManager(models.Manager):
    def visible_to_user(self, user):
        if user.is_superuser:
            return self.all()
        return self.filter(
            models.Q(is_publicly_visible=True, is_approved=True)
            | models.Q(user_id=user.pk)
        )


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    first_name = models.CharField(
        max_length=200, validators=[validate_sluggable_name], verbose_name="First Name"
    )
    last_name = models.CharField(
        max_length=200, validators=[validate_sluggable_name], verbose_name="Last Name"
    )
    slug = sluggable_fields.SluggableField(
        decider=ProfileSlug,
        populate_from="get_full_name",
        slugify=slugify_user,
        unique=True,
    )
    job_title = models.CharField(max_length=1024, blank=True, verbose_name="Job Title")
    organization = models.CharField(max_length=1024, blank=True)
    study_subject = models.CharField(max_length=1024, blank=True)
    image = thumbnail.ImageField(
        upload_to=upload_path.auto_cleaned_path_stripped_uuid4, blank=True
    )
    linkedin_url = models.URLField(max_length=400, blank=True, verbose_name="Linkedin")
    facebook_url = models.URLField(max_length=400, blank=True, verbose_name="Facebook")
    calendly_url = models.CharField(max_length=512, blank=True)
    twitter = models.CharField(max_length=512, blank=True)
    personal_website_url = models.URLField(
        max_length=400, blank=True, verbose_name="Personal Website"
    )

    city_or_town = models.CharField(max_length=100, blank=True, verbose_name="City")
    country = models.CharField(max_length=100, blank=True)
    lat = models.FloatField(null=True, blank=True, default=None)
    lon = models.FloatField(null=True, blank=True, default=None)

    available_to_volunteer = models.BooleanField(blank=True, default=False)
    open_to_job_offers = models.BooleanField(blank=True, default=False)
    is_hiring = models.BooleanField(blank=True, default=False)
    available_as_speaker = models.BooleanField(blank=True, default=False)
    email_visible = models.BooleanField(default=False)
    allow_messaging = models.BooleanField(
        default=True,
        verbose_name="Allow approved users to message me",
        help_text="Your email address won't be visible to them",
    )

    summary = models.TextField(
        blank=True, validators=[MaxLengthValidator(6000)], verbose_name="Bio"
    )
    offering = models.TextField(blank=True, validators=[MaxLengthValidator(2000)])
    looking_for = models.TextField(blank=True, validators=[MaxLengthValidator(2000)])
    topics_i_speak_about = models.TextField(
        blank=True,
        validators=[MaxLengthValidator(2000)],
        verbose_name="Topics I Speak About",
    )

    local_groups = models.ManyToManyField(
        LocalGroup, through="Membership", blank=True, verbose_name="EA Groups"
    )
    visibility = EnumField(
        VisibilityEnum,
        max_length=16,
        default=VisibilityEnum.PUBLIC,
        verbose_name="Profile visibility",
    )
    slugs = contenttypes_fields.GenericRelation(ProfileSlug)

    tags_generic = models.ManyToManyField(
        ProfileTag,
        limit_choices_to={"types__type": ProfileTagTypeEnum.GENERIC},
        blank=True,
        related_name="tags_generic",
    )
    tags_affiliation = models.ManyToManyField(
        ProfileTag,
        limit_choices_to={"types__type": ProfileTagTypeEnum.AFFILIATION},
        blank=True,
        related_name="tags_affiliation",
    )
    tags_cause_area = models.ManyToManyField(
        ProfileTag,
        limit_choices_to={"types__type": ProfileTagTypeEnum.CAUSE_AREA},
        blank=True,
        related_name="tags_cause_area",
    )
    tags_cause_area_expertise = models.ManyToManyField(
        ProfileTag,
        limit_choices_to={"types__type": ProfileTagTypeEnum.CAUSE_AREA_EXPERTISE},
        blank=True,
        related_name="tags_cause_area_expertise",
    )
    tags_expertise_area = models.ManyToManyField(
        ProfileTag,
        limit_choices_to={"types__type": ProfileTagTypeEnum.EXPERTISE_AREA},
        blank=True,
        related_name="tags_expertise_area",
    )
    tags_organisational_affiliation = models.ManyToManyField(
        ProfileTag,
        limit_choices_to={"types__type": ProfileTagTypeEnum.ORGANISATIONAL_AFFILIATION},
        blank=True,
        related_name="tags_organisational_affiliation",
    )
    tags_career_interest = models.ManyToManyField(
        ProfileTag,
        limit_choices_to={"types__type": ProfileTagTypeEnum.CAREER_INTEREST},
        blank=True,
        related_name="tags_career_interest",
    )
    tags_speech_topic = models.ManyToManyField(
        ProfileTag,
        limit_choices_to={"types__type": ProfileTagTypeEnum.SPEECH_TOPIC},
        blank=True,
        related_name="tags_speech_topic",
    )
    tags_pledge = models.ManyToManyField(
        ProfileTag,
        limit_choices_to={"types__type": ProfileTagTypeEnum.PLEDGE},
        blank=True,
        related_name="tags_pledge",
    )
    tags_university = models.ManyToManyField(
        ProfileTag,
        limit_choices_to={"types__type": ProfileTagTypeEnum.UNIVERSITY},
        blank=True,
        related_name="tags_university",
    )
    tags_event_attended = models.ManyToManyField(
        ProfileTag,
        limit_choices_to={"types__type": ProfileTagTypeEnum.EVENT_ATTENDED},
        blank=True,
        related_name="tags_event_attended",
    )
    tags_career_stage = models.ManyToManyField(
        ProfileTag,
        limit_choices_to={"types__type": ProfileTagTypeEnum.CAREER_STAGE},
        blank=True,
        related_name="tags_career_stage",
    )
    tags_ea_involvement = models.ManyToManyField(
        ProfileTag,
        limit_choices_to={"types__type": ProfileTagTypeEnum.EA_INVOLVEMENT},
        blank=True,
        related_name="tags_ea_involvement",
    )

    objects = ProfileManager()

    # legacy fields
    is_public = models.BooleanField(
        default=True,
        verbose_name="Visible profile",
        help_text="Unchecking this will conceal your profile from everyone. While visible profiles are searchable on the web.",
    )
    legacy_record = models.PositiveIntegerField(
        null=True, default=None, editable=False, unique=True
    )
    cause_areas = postgres_fields.ArrayField(
        enum.EnumField(CauseArea), blank=True, default=list
    )
    cause_areas_other = models.TextField(
        blank=True, validators=[MaxLengthValidator(2000)]
    )
    expertise_areas = postgres_fields.ArrayField(
        enum.EnumField(ExpertiseArea), blank=True, default=list
    )
    expertise_areas_other = models.TextField(
        blank=True, validators=[MaxLengthValidator(2000)]
    )
    career_interest_areas = postgres_fields.ArrayField(
        enum.EnumField(ExpertiseArea), blank=True, default=list
    )
    organisational_affiliations = postgres_fields.ArrayField(
        enum.EnumField(OrganisationalAffiliation), blank=True, default=list
    )
    giving_pledges = postgres_fields.ArrayField(
        enum.EnumField(GivingPledge), blank=True, default=list
    )

    class Meta:
        ordering = ["first_name", "slug"]

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        return urls.reverse("profiles_app:profile", args=[self.slug])

    def get_messaging_url_if_can_receive_message(self) -> str:
        if self.is_can_receive_message():
            return urls.reverse("profiles_app:message_profile", args=[self.slug])
        return ""

    def geocode(self):
        self.lat = None
        self.lon = None
        if self.city_or_town and self.country:
            geocoders.options.default_user_agent = "eahub"
            location = geocoders.Nominatim(timeout=10).geocode(
                f"{self.city_or_town}, {self.country}"
            )
            if location:
                self.lat = location.latitude
                self.lon = location.longitude
        return self

    def get_full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    def get_image_url(self) -> Optional[str]:
        if self.image:
            return get_thumbnail(self.image, "200x200", crop="center").url
        else:
            return None

    def is_searchable_public(self) -> bool:
        return (
            self.is_approved
            and self.visibility == VisibilityEnum.PUBLIC
            and self.user.is_active
        )

    def is_searchable_internal(self) -> bool:
        return (
            self.is_approved
            and self.visibility in [VisibilityEnum.INTERNAL, VisibilityEnum.PUBLIC]
            and self.user.is_active
        )

    def is_can_receive_message(self) -> bool:
        return (
            self.is_approved
            and self.visibility in [VisibilityEnum.PUBLIC, VisibilityEnum.INTERNAL]
            and self.allow_messaging
        )

    def is_organiser(self) -> bool:
        return self.user.localgroup_set.exists()

    def get_tags_cause_area_formatted(self) -> List[str]:
        return [tag.name for tag in self.tags_cause_area.all()]

    def get_tags_generic_formatted(self) -> List[str]:
        return [tag.name for tag in self.tags_generic.all()]

    def get_tags_affiliation_formatted(self) -> List[str]:
        return [tag.name for tag in self.tags_affiliation.all()]

    def get_tags_cause_area_expertise_formatted(self) -> List[str]:
        return [tag.name for tag in self.tags_cause_area_expertise.all()]

    def get_tags_expertise_formatted(self) -> List[str]:
        return [tag.name for tag in self.tags_expertise_area.all()]

    def get_tags_organisational_affiliation_formatted(self) -> List[str]:
        return [tag.name for tag in self.tags_organisational_affiliation.all()]

    def get_tags_career_interest_formatted(self) -> List[str]:
        return [tag.name for tag in self.tags_career_interest.all()]

    def get_tags_pledge_formatted(self) -> List[str]:
        return [tag.name for tag in self.tags_pledge.all()]

    def get_tags_event_attended_formatted(self) -> List[str]:
        return [tag.name for tag in self.tags_event_attended.all()]

    def get_tags_speech_topic_formatted(self) -> List[str]:
        return [tag.name for tag in self.tags_speech_topic.all()]

    def get_local_groups_formatted(self) -> List[str]:
        return [group.name for group in self.local_groups.all()]

    def get_organizer_of_local_groups_formatted(self) -> List[str]:
        return [group.name for group in self.user.localgroup_set.all()]

    def get_image_placeholder(self) -> str:
        return f"Avatar{self.id % 10}.jpg"

    def is_publicly_visible(self) -> bool:
        return self.visibility == VisibilityEnum.PUBLIC

    def is_private(self) -> bool:
        return self.visibility == VisibilityEnum.PRIVATE


class ProfileInternal(Profile):
    pass


class ProfileAnalyticsLog(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    field = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    action_uuid = models.UUIDField(default=uuid.uuid4)
    old_value = models.TextField()
    new_value = models.TextField()


class Membership(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    local_group = models.ForeignKey(LocalGroup, on_delete=models.CASCADE)
