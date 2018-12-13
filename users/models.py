from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    # inherit django user object
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    email = models.EmailField(blank=True, null=True, unique=True)
    REQUIRED_FIELDS = []
    # add custom fields
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True)