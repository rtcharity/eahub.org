import autoslug
from django import urls
from django.conf import settings
from django.contrib.postgres import fields as postgres_fields
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
    name = models.CharField(
        "name of group",
        max_length=100,
        help_text="University groups: Ideally avoid acronyms in your group name unless "
        "they are likely to be unique worldwide. If the name of your "
        "university is also the name of a city, indicate in the name that "
        "this is a university group.",
    )
    is_active = models.BooleanField(default=True)
    organisers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="Organisership", blank=True
    )
    local_group_type = enum.EnumField(
        LocalGroupType, null=True, blank=True, default=None
    )
    local_group_types = postgres_fields.ArrayField(
        enum.EnumField(LocalGroupType), blank=True, default=list
    )
    city_or_town = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    lat = models.FloatField(null=True, blank=True, default=None)
    lon = models.FloatField(null=True, blank=True, default=None)
    website = models.URLField(blank=True)
    other_website = models.URLField(blank=True)
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
    other_info = models.TextField(blank=True, validators=[MaxLengthValidator(5000)])

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

    def organisers_names(self):
        return ", ".join([user.profile.name for user in self.organisers.all()])

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

    def get_local_group_types(self):
        if self.local_group_types:
            return ", ".join(map(LocalGroupType.label, self.local_group_types))
        else:
            return "Other"

    def convert_to_row(self, field_names):
        values = []
        for field in field_names:
            if field == "local_group_types":
                values.append(self.get_local_group_types())
            elif field == "organisers":
                values.append(self.organisers_names())
            else:
                values.append(getattr(self, field))
        return values


class Organisership(models.Model):
    local_group = models.ForeignKey(LocalGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
