import json
from django.core import validators
from django.db import models
from django.contrib.postgres.fields import ArrayField
from geopy.geocoders import Nominatim
from ..profiles.models import Profile
geolocator = Nominatim(timeout=10)


# methods to maintain consistency in model design
def _choice_field(choices):
    return models.CharField(
        max_length=max([len(x[0]) for x in choices]),
        choices=choices,
        null=True, blank=True
    )
def _choices_field(choices):
    return ArrayField(
        _choice_field(choices),        
        default=list
    )
def _other_field():
    return models.TextField(null=True, blank=True)


class Group(models.Model):

    GROUP_TYPE_CHOICES = [
        ('COUNTRY', 'Country'),
        ('CITY', 'City'),
        ('UNIVERSITY', 'University'),
        ('OTHER', 'Other')
    ]

    # fields
    name = models.CharField(max_length=100)
    group_type, group_type_other = _choice_field(GROUP_TYPE_CHOICES), _other_field()
    summary = models.TextField(null=True, blank=True)
    organisers = models.ManyToManyField(Profile, blank=True)
    city_or_town = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=200, null=True, blank=True)
    facebook_group = models.CharField(max_length=200, null=True, blank=True)
    facebook_page = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    meetup_details = models.TextField(null=True, blank=True)
    meetups_per_month = models.IntegerField(null=True, blank=True)
    meetup_url = models.CharField(max_length=200, null=True, blank=True)
    lat = models.DecimalField(
        # set programatically by geocode()
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    lon = models.DecimalField(
        # set programatically by geocode()
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    airtable_record = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default=None,
        unique=True,
        validators=[validators.MinLengthValidator(1)],
    )

    # table of donations
    # example: {"donations":[{"amount":"a", "to":"b", "when":"c", "details":"d"}]}
    donations = models.TextField(null=True, blank=True)
    def get_donations(self):
        if not self.donations: return []
        return json.loads(self.donations)['donations']

    # list of links
    # example: {"links":[{"link":"a", "label":"b"}]}
    links = models.TextField(null=True, blank=True)
    def get_links(self):
        if not self.links: return []
        return json.loads(self.links)['links']

    # list of links
    # example: {"images": ["a", "b"]}
    images = models.TextField(null=True, blank=True)

    def location(self):
        return ', '.join([
            x
            for x in [self.city_or_town, self.country]
            if x not in [None, '']
        ])
    def geocode(self):
        location = ', '.join([str(self.city_or_town), str(self.country)])
        if len(location) > 0: 
            location = geolocator.geocode(location)
            self.lat = location.latitude if location else None
            self.lon = location.longitude if location else None
            return self
        else:
            self.lat = None
            self.lon = None
            return self


    # edit history
    # example: [{"date":"10/10/2001","user": "user_1 user@domain.com", diff":{"name":{"before":"EA Londonzzz","after":"EA London"}}}]
    edit_history = models.TextField(default='[]')
    def get_edit_history(self):
        if not self.edit_history: return []
        return json.loads(self.edit_history)
