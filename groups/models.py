import json
from django.db import models
from django.contrib.postgres.fields import ArrayField
from profiles.models import Profile

class Group(models.Model):

    GROUP_TYPE_CHOICES = [
        ('COUNTRY', 'Country'),
        ('CITY', 'City'),
        ('UNIVERSITY', 'University')
    ]

    # fields
    name = models.CharField(max_length=100)
    group_type = models.CharField(max_length=200, null=True, blank=True, choices=GROUP_TYPE_CHOICES)
    summary = models.TextField(null=True, blank=True)
    organisers = models.ManyToManyField(Profile, blank=True)
    city_or_town = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=200, null=True, blank=True)
    facebook_group = models.CharField(max_length=200, null=True, blank=True)
    facebook_page = models.CharField(max_length=200, null=True, blank=True)
    official_email = models.CharField(max_length=200, null=True, blank=True)
    meetup_details = models.TextField(null=True, blank=True)
    meetups_per_month = models.IntegerField(null=True, blank=True)
    meetup_url = models.CharField(max_length=200, null=True, blank=True)
    total_group_donations = models.IntegerField(null=True, blank=True)

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

    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    def location(self):
        return ', '.join([
            x
            for x in [self.city_or_town, self.country]
            if x not in [None, '']
        ])

    # edit history
    # example: [{"date":"10/10/2001","user": "user_1 user@domain.com", diff":{"name":{"before":"EA Londonzzz","after":"EA London"}}}]
    edit_history = models.TextField(default='[]')
    def get_edit_history(self):
        if not self.edit_history: return []
        return json.loads(self.edit_history)
