import string
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser, UserManager
from django_upload_path.upload_path import auto_cleaned_path_stripped_uuid4
from geopy.geocoders import Nominatim
from sorl.thumbnail import ImageField

geolocator = Nominatim(timeout=10)


# methods to maintain consistency in model design
def _choices_field(choices):
    return ArrayField(
        models.CharField(
            max_length=max([len(x[0]) for x in choices]),
            choices=choices,
            null=True, blank=True,
        ),        
        default=list
    )
def _other_field():
    return models.TextField(null=True, blank=True)


class ProfileManager(UserManager):
    pass


class Profile(AbstractUser):

    objects = ProfileManager()
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []

    EXPERTISE_CHOICES = [
        ('MANAGEMENT', 'Management'),
        ('OPERATIONS', 'Operations'),
        ('RESEARCH', 'Research'),
        ('GOVERNMENT_AND_POLICY', 'Government and policy'),
        ('ENTREPRENEURSHIP', 'Entrepreneurship'),
        ('SOFTWARE_ENGINEERING', 'Software engineering'),
        ('AI_TECHNICAL_EXPERTISE', 'AI technical expertise'),
        ('MATH_QUANT_STATS_EXPERTISE', 'Math, quant, stats expertise'),
        ('ECONOMICS, QUANTITATIVE SOCIAL SCIENCE', 'Economics, quantitative social science'),
        ('MOVEMENT_BUILDING', 'Movement building'),
        ('COMMUNICATIONS', 'Communications'),
        ('OTHER', 'Other'),
    ]
    CAUSE_AREA_CHOICES = [
        ('GLOBAL_POVERTY', 'Global Poverty'),
        ('ANIMAL_WELFARE_AND_RIGHTS', 'Animal Welfare/Rights'),
        ('LONG_TERM_FUTURE', 'Long-term Future'),
        ('CAUSE_PRIORITISATION', 'Cause Prioritisation'),
        ('META', 'Meta'),
        ('OTHER', 'Other'),
    ]

    # personal information
    summary = models.TextField(null=True, blank=True)
    image = ImageField(blank=True, upload_to=auto_cleaned_path_stripped_uuid4)
    city_or_town = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    # lat & lon programatically set by geocode()
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name='latitude')
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name='longitude')
    
    # settings & privacy
    gdpr_confirmed = models.BooleanField(
        # used to activate account after hubreboot
        default=True
    )

    # cause_areas
    cause_areas, cause_areas_other = _choices_field(CAUSE_AREA_CHOICES), _other_field()
    available_to_volunteer = models.BooleanField(default=None, null=True)

    # career
    open_to_job_offers = models.BooleanField(default=None, null=True)
    expertise, expertise_other = _choices_field(EXPERTISE_CHOICES), _other_field()

    # community
    available_as_speaker = models.BooleanField(default=None, null=True)
    topics_i_speak_about = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return string.capwords(' '.join([self.first_name, self.last_name]))

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
