import autoslug
from django.core import validators
from django.db import models
from django_enumfield import enum


class LocalGroupType(enum.Enum):

    CITY = 1
    COUNTRY = 2
    UNIVERSITY = 3

    labels = {
        CITY: "City",
        COUNTRY: "Country",
        UNIVERSITY: "University",
    }


class LocalGroup(models.Model):
    slug = autoslug.AutoSlugField(populate_from="name", unique=True)
    name = models.CharField(max_length=100)
    local_group_type = enum.EnumField(
        LocalGroupType, null=True, blank=True, default=None
    )
    city_or_town = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    lat = models.FloatField(null=True, blank=True, default=None)
    lon = models.FloatField(null=True, blank=True, default=None)
    website = models.URLField(blank=True)
    facebook_group = models.URLField(blank=True)
    facebook_page = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    meetup_url = models.URLField(blank=True)
    airtable_record = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default=None,
        unique=True,
        validators=[validators.MinLengthValidator(1)],
    )
