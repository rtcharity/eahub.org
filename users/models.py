from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class ProfileManager(UserManager):
    pass

class Profile(AbstractUser):
    # inherit django user object
    objects = ProfileManager()
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []
    # add custom fields
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True)