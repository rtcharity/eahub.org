from django.db import models
from django.contrib.postgres.fields import ArrayField
from profiles.models import Profile

class Group(models.Model):
    
    # fields
    name = models.CharField(max_length=100)
    summary = models.TextField(null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    organisers = models.ManyToManyField(Profile)
    city_or_town = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    website = models.CharField(max_length=200, null=True)
    facebook_group = models.CharField(max_length=200, null=True)
    facebook_page = models.CharField(max_length=200, null=True)
    official_email = models.CharField(max_length=200, null=True)
    lean_email = models.CharField(max_length=200, null=True)
    meetup_details = models.TextField(null=True)
    meetup_url = models.CharField(max_length=200, null=True)
    serves_as = models.TextField(null=True)

    # table of donations
    # example: {"donations":[{"Amount":"a","To":"b","When":"c","Any details (e.g. who donated)":"d"}]}
    donations = models.TextField(null=True)
    
    # list of links
    # example: {"links":[{"href":"a","label":"b"}]}
    links = models.TextField(null=True)

    # list of links
    # example: {"images": ["a", "b"]}
    images = models.TextField(null=True)