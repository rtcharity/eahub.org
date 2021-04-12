from typing import Type

from django.db import models
from djmoney.models.fields import CurrencyField
from djmoney.settings import CURRENCY_CHOICES
from enumfields import Enum, EnumField

from eahub.profiles.models import Profile
from eahub.tags.models import Tag


class JobStatus(Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_INFO = "needs_info"


class JobTagTypeEnum(Enum):
    SKILL = "skill"
    AREA = "area"
    TYPE = "type"
    LOCATION = "location"


class JobTagType(models.Model):
    type = EnumField(JobTagTypeEnum, max_length=128, unique=True)

    def __str__(self):
        return str(self.type)


class JobTagStatus(Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING = "pending"


class JobTag(Tag):
    types = models.ManyToManyField(JobTagType)
    status = EnumField(JobTagStatus, default=JobTagStatus.APPROVED, max_length=64)
    tag_type_enum = JobTagTypeEnum

    def get_model(self) -> Type[models.Model]:
        return Job


class JobVisibility(Enum):
    PUBLIC = "public"
    # INTERNAL = "internal"
    INVISIBLE = "invisible"


class Job(models.Model):
    title = models.CharField(max_length=256, null=True)
    company = models.CharField(max_length=256, null=True)
    company_logo = models.ImageField(null=True)
    description_teaser = models.CharField(max_length=512, null=True)
    description = models.TextField(null=True)

    experience_min = models.PositiveIntegerField(null=True, blank=True)
    experience_max = models.PositiveIntegerField(null=True, blank=True)

    salary_min = models.PositiveIntegerField(null=True, blank=True)
    salary_max = models.PositiveIntegerField(null=True, blank=True)
    salary_currency = CurrencyField(choices=CURRENCY_CHOICES, blank=True, default="USD")

    tags_location = models.ManyToManyField(
        JobTag,
        limit_choices_to={"types__type": JobTagTypeEnum.LOCATION},
        blank=True,
        related_name="tags_location",
    )
    tags_skill = models.ManyToManyField(
        JobTag,
        limit_choices_to={"types__type": JobTagTypeEnum.SKILL},
        blank=True,
        related_name="tags_skill",
    )
    tags_area = models.ManyToManyField(
        JobTag,
        limit_choices_to={"types__type": JobTagTypeEnum.AREA},
        blank=True,
        related_name="tags_area",
    )
    tags_type = models.ManyToManyField(
        JobTag,
        limit_choices_to={"types__type": JobTagTypeEnum.TYPE},
        blank=True,
        related_name="tags_type",
    )

    author = models.ForeignKey(
        Profile, blank=False, null=True, on_delete=models.SET_NULL
    )
    visibility = EnumField(
        JobVisibility,
        default=JobVisibility.PUBLIC,
        max_length=256,
    )
    status = EnumField(
        JobStatus,
        default=JobStatus.DRAFT,
        max_length=256,
    )
    is_visa_sponsor = models.BooleanField(default=False, verbose_name="Visa sponsoring")
    is_remote_only = models.BooleanField(default=False, verbose_name="Remote only")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title
