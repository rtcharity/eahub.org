from django.db import models
from solo.models import SingletonModel


class FeedbackURLConfig(SingletonModel):
    site_url = models.URLField("feedback.eahub.org")

    def __str__(self):
        return "Feedback URL"

    class Meta:
        verbose_name = "Feedback URL"