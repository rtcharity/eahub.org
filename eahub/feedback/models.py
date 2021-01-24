from django.db import models

class Feedback(models.Model):
    email = models.CharField(blank=True, max_length=254)
    message = models.CharField(max_length=5000, blank=False)
    page_url = models.CharField(blank=True, max_length=2048)
    creation_time = models.DateTimeField(
        auto_now=True, null=True, blank=True, editable=False
    )
