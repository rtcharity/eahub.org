import autoslug
from django import urls
from django.conf import settings
from django.contrib.postgres import fields as postgres_fields
from django.core import validators
from django.core.cache import cache
from django.core.validators import MaxLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_enumfield import enum
from flags.state import flag_enabled
from geopy import geocoders

from eahub.base.models import User


class LocalGroupType(enum.Enum):

    CITY = 1
    COUNTRY = 2
    UNIVERSITY = 3

    labels = {CITY: "City", COUNTRY: "National/Regional", UNIVERSITY: "University"}


class LocalGroup(models.Model):

    slug = autoslug.AutoSlugField(populate_from="name", unique=True)
    is_public = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    organisers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="Organisership", blank=True
    )
    organisers_freetext = models.CharField(
        "Organisers (Non EA Hub members)", max_length=100, blank=True
    )
    local_group_type = enum.EnumField(
        LocalGroupType, null=True, blank=True, default=None
    )
    local_group_types = postgres_fields.ArrayField(
        enum.EnumField(LocalGroupType), blank=True, default=list
    )
    city_or_town = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
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
        profile_names = []
        for user in self.organisers.all():
            try:
                profile_names.append(user.profile.get_full_name())
            except User.profile.RelatedObjectDoesNotExist:
                profile_names.append("User profile missing")
        return ", ".join(profile_names)

    def organisers_emails(self):
        return ", ".join([user.email for user in self.organisers.all()])

    def has_organisers_with_messaging_enabled(self):
        return (
            len(
                [
                    user
                    for user in self.organisers.all()
                    if user.profile.is_can_receive_message()
                ]
            )
            > 0
        )

    def get_messaging_emails(self, request):
        if not self.email and flag_enabled("MESSAGING_FLAG", request=request):
            return [
                user.email
                for user in self.organisers.all()
                if user.profile.allow_messaging
            ]
        elif self.email:
            return [self.email]

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

    def get_local_group_types(self):
        if self.local_group_types:
            return ", ".join(map(LocalGroupType.label, self.local_group_types))
        else:
            return "Other"


@receiver(post_save, sender=LocalGroup)
def clear_the_cache(**kwargs):
    cache.clear()


class Organisership(models.Model):
    local_group = models.ForeignKey(LocalGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
