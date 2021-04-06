from django.db import models


class Feedback(models.Model):
    email = models.CharField(
        blank=True, max_length=254, verbose_name="Email (optional)"
    )
    message = models.TextField(blank=False, verbose_name="Feedback")
    page_url = models.CharField(blank=True, max_length=2048)
    creation_time = models.DateTimeField(auto_now_add=True)
