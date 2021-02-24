from authtools import models as authtools_models
from django.core.validators import URLValidator
from django.db import models
from solo.models import SingletonModel


class User(authtools_models.AbstractEmailUser):
    def has_profile(self):
        return hasattr(self, "profile")


class FeedbackURLConfig(SingletonModel):
    site_url = models.TextField(
        default="feedback.eahub.org", validators=[URLValidator()]
    )

    def __str__(self):
        return "Feedback URL"

    class Meta:
        verbose_name = "Feedback URL"


class MessagingLog(models.Model):
    sender_email = models.EmailField(max_length=254)
    recipient_email = models.EmailField(max_length=254)
    send_action_guid = models.UUIDField(default=uuid.uuid4)
    time = models.DateTimeField(default=timezone.now)