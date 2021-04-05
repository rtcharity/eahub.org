from typing import Type

from django.db import models
from enumfields import Enum
from enumfields import EnumField

from eahub.tags.models import Tag


class JobTagTypeEnum(Enum):
    SKILL = "skill"
    MARKET = "market"
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
    title = models.CharField(max_length=256)
    company = models.CharField(max_length=256)
    company_logo = models.ImageField()
    description_teaser = models.CharField(max_length=512)
    description = models.TextField()

    experience_min = models.PositiveIntegerField(null=True)
    experience_max = models.PositiveIntegerField(null=True)
    salary_min = models.PositiveIntegerField(null=True)
    salary_max = models.PositiveIntegerField(null=True)

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
    tags_market = models.ManyToManyField(
        JobTag,
        limit_choices_to={"types__type": JobTagTypeEnum.MARKET},
        blank=True,
        related_name="tags_market",
    )
    tags_type = models.ManyToManyField(
        JobTag,
        limit_choices_to={"types__type": JobTagTypeEnum.TYPE},
        blank=True,
        related_name="tags_type",
    )
    
    visibility = EnumField(
        JobVisibility, default=JobVisibility.PUBLIC, max_length=256,
    )
    is_immigration_support = models.BooleanField(default=False)
    is_remote = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
