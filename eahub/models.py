from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True)


class Group(models.Model):
    name = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    organiser = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    city_or_town = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    website = models.CharField(max_length=200, null=True)
    facebook_group = models.CharField(max_length=200, null=True)
    facebook_page = models.CharField(max_length=200, null=True)