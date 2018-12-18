import json
from django.db import models
from django.contrib.postgres.fields import ArrayField
from profiles.models import Profile

class Group(models.Model):
    
    # fields
    name = models.CharField(max_length=100)
    summary = models.TextField(null=True)
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

    # table of donations
    # example: {"donations":[{"amount":"a", "to":"b", "when":"c", "details":"d"}]}
    donations = models.TextField(null=True)
    def get_donations(self):
        if not self.donations: return []
        return json.loads(self.donations)['donations']
    
    # list of links
    # example: {"links":[{"link":"a", "label":"b"}]}
    links = models.TextField(null=True)
    def get_links(self):
        if not self.links: return []
        return json.loads(self.links)['links']

    # list of links
    # example: {"images": ["a", "b"]}
    images = models.TextField(null=True)

    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    def location(self):
        return ', '.join([
            x
            for x in [self.city_or_town, self.country]
            if x not in [None, '']
        ])