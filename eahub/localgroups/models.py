import autoslug
from django import urls
from django.conf import settings
from django.core import validators
from django.core.validators import MaxLengthValidator
from django.db import models
from django_enumfield import enum
from geopy import geocoders


class LocalGroupType(enum.Enum):

    CITY = 1
    COUNTRY = 2
    UNIVERSITY = 3

    labels = {CITY: "City", COUNTRY: "Country", UNIVERSITY: "University"}


class LocalGroup(models.Model):

    slug = autoslug.AutoSlugField(populate_from="name", unique=True)
    is_public = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    organisers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="Organisership", blank=True
    )
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
    last_edited = models.DateTimeField(
        auto_now=True, null=True, blank=True, editable=False
    )

    class Meta:
        ordering = ["name", "slug"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return urls.reverse("group", args=[self.slug])

    def public_organisers(self):
        return self.organisers.filter(profile__is_public=True).order_by(
            "profile__name", "profile__slug"
        )

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


class Organisership(models.Model):
    local_group = models.ForeignKey(LocalGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
