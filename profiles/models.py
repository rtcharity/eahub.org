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
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, verbose_name='latitude')
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, verbose_name='longitude')
    city_or_town = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'