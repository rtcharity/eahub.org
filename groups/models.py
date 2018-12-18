from django.db import models
from profiles.models import Profile

class Group(models.Model):
    
    # fields
    name = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    organiser = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    city_or_town = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    website = models.CharField(max_length=200, null=True)
    facebook_group = models.CharField(max_length=200, null=True)
    facebook_page = models.CharField(max_length=200, null=True)
    official_email = models.CharField(max_length=200, null=True)
    lean_email = models.CharField(max_length=200, null=True)