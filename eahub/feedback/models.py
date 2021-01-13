from django.db import models

## added by Lisa
class Feedback(models.Model):
    email = models.CharField(blank=True, max_length=30)
    message = models.CharField(max_length=2000)
    page_url = models.CharField(blank=True, max_length=50)
