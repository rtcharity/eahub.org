import uuid


from authtools import models as authtools_models
from django.core.validators import URLValidator
from django.db import models
from django.utils import timezone
from solo.models import SingletonModel


class User(authtools_models.AbstractEmailUser):
    def has_profile(self):
        return hasattr(self, "profile")


class FeedbackURLConfig(SingletonModel):
    site_url = models.TextField(
        default="https://feedback.eahub.org", validators=[URLValidator()]
    )

    def __str__(self):
        return "Feedback URL"

    class Meta:
        verbose_name = "Feedback URL"


class MessagingLog(models.Model):
    USER = "USER"
    GROUP = "GROUP"
    RECIPIENT_TYPE_CHOICES = [
        (USER, "User"),
        (GROUP, "Group"),
    ]
    sender_email = models.EmailField(max_length=254)
    recipient_email = models.EmailField(max_length=254)
    recipient_type = models.CharField(
        max_length=5,
        choices=RECIPIENT_TYPE_CHOICES,
        default=USER,
    )
    send_action_uuid = models.UUIDField(default=uuid.uuid4)
    time = models.DateTimeField(default=timezone.now)
