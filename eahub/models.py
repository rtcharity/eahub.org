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