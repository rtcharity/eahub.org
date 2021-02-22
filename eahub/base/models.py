from authtools import models as authtools_models
from django.core.validators import URLValidator
from django.db import models
from solo.models import SingletonModel


class User(authtools_models.AbstractEmailUser):
    def has_profile(self):
        return hasattr(self, "profile")


class FeedbackURLConfig(SingletonModel):
    site_url = models.TextField(default="feedback.eahub.org", validators=[URLValidator()])

    def __str__(self):
        return "Feedback URL"

    class Meta:
        verbose_name = "Feedback URL"