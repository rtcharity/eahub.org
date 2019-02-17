import string, csv
from django.db import models
from django.contrib.postgres.fields import ArrayField, CIEmailField
from django.contrib.auth.models import AbstractUser, UserManager
from django_upload_path.upload_path import auto_cleaned_path_stripped_uuid4
from geopy.geocoders import Nominatim
from sorl.thumbnail import ImageField
geolocator = Nominatim(timeout=10)


# methods to maintain consistency in model design
def _choice_field(choices):
    return models.CharField(
        max_length=max([len(x[0]) for x in choices]),
        choices=choices,
        null=True, blank=True
    )
def _choices_field(choices):
    return ArrayField(
        _choice_field(choices),
        default=list
    )
def _other_field():
    return models.TextField(null=True, blank=True)


class ProfileManager(UserManager):
    pass


class Profile(AbstractUser):

    objects = ProfileManager()
    USERNAME_FIELD = 'email'
    email = CIEmailField(unique=True)
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
    GIVING_PLEDGE_CHOICES = [
        ('', 'No'),
        ('GIVING_WHAT_WE_CAN', 'Giving What We Can'),
        ('THE_LIFE_YOU_CAN_CHANGE', 'The Life You Can Save'),
        ('ONE_FOR_THE_WORLD', 'One for the World'),
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
    def get_pretty_cause_areas(self):
        return ', '.join([
            [label for choice, label in self.CAUSE_AREA_CHOICES if choice==cause_area][0]
            for cause_area in self.cause_areas
            if cause_area != 'OTHER'
        ])
    giving_pledge, giving_pledge_other = _choice_field(GIVING_PLEDGE_CHOICES), _other_field()

    # career
    open_to_job_offers = models.BooleanField(default=None, null=True)
    expertise, expertise_other = _choices_field(EXPERTISE_CHOICES), _other_field()
    def get_pretty_expertise(self):
        return ', '.join([
            [label for choice, label in self.EXPERTISE_CHOICES if choice==expertise][0]
            for expertise in self.expertise
            if expertise != 'OTHER'
        ])

    # community
    available_as_speaker = models.BooleanField(default=None, null=True)
    topics_i_speak_about = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return string.capwords(' '.join([self.first_name, self.last_name]))

    def csv(self, response):
        writer = csv.writer(response)
        writer.writerows([
            ['profile_id', self.id],
            ['first_name', self.first_name],
            ['last_name', self.last_name],
            ['email', self.email],
            ['summary', self.summary],
            ['city_or_town', self.city_or_town],
            ['country', self.country],
            ['gdpr_confirmed', self.gdpr_confirmed],
            ['cause_areas', self.get_pretty_cause_areas()],
            ['cause_areas_other', self.cause_areas_other],
            ['available_to_volunteer', self.available_to_volunteer],
            ['giving_pledge', self.giving_pledge],
            ['giving_pledge_other', self.giving_pledge_other],
            ['open_to_job_offers', self.open_to_job_offers],
            ['expertise', self.get_pretty_expertise()],
            ['expertise_other', self.expertise_other],
            ['available_as_speaker', self.available_as_speaker],
            ['topics_i_speak_about', self.topics_i_speak_about],
        ])
        return response

    def location(self):
        return ', '.join([
            x
            for x in [self.city_or_town, self.country]
            if x not in [None, '']
        ])

    def geocode(self):
        location = ', '.join([str(self.city_or_town), str(self.country)])
        if len(location) > 0: 
            location = geolocator.geocode(location)
            self.lat = location.latitude if location else None
            self.lon = location.longitude if location else None
            return self
        else:
            self.lat = None
            self.lon = None
            return self

    def image_placeholder(self):
        # maintains the same image whenever users log in
        return 'Avatar{}.png'.format(str(self.id)[-1])

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
