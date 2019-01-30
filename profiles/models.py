from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from geopy.geocoders import Nominatim
geolocator = Nominatim()


class ProfileManager(UserManager):
    pass


class Profile(AbstractUser):

    # inherit django user object
    objects = ProfileManager()
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []

    # add custom fields
    city_or_town = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True) 
    lat = models.DecimalField(
        # set programatically by geocode()
        max_digits=9, decimal_places=6, null=True, blank=True, verbose_name='latitude'
    )
    lon = models.DecimalField(
        # set programatically by geocode()
        max_digits=9, decimal_places=6, null=True, blank=True, verbose_name='longitude'
    )   
    gdpr_confirmed = models.BooleanField(
        # notes = used to activate account after hubreboot
        default=True
    )
    cause_areas = models.CharField(max_length=100, null=True, blank=True)
    job_status = models.CharField(max_length=100, null=True, blank=True)
    expertise = models.CharField(max_length=100, null=True, blank=True)
    skills = models.CharField(max_length=100, null=True, blank=True)
    speaker = models.CharField(max_length=100, null=True, blank=True)
    volunteer = models.CharField(max_length=100, null=True, blank=True)
    org_affiliations = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return ' '.join([
            x.title()
            for x in [self.first_name, self.last_name]
            if x not in [None, '']
        ])

    def location(self):
        return ', '.join([
            x
            for x in [self.city_or_town, self.country]
            if x not in [None, '']
        ])

    def geocode(self):
        location = ', '.join([str(self.city_or_town), str(self.country)])
        location = geolocator.geocode(location)
        self.lat = location.latitude if location else None
        self.lon = location.longitude if location else None
        return self

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
