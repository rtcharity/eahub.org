from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import FeedbackURLConfig

admin.site.register(FeedbackURLConfig, SingletonModelAdmin)
