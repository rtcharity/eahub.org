## added by Lisa
from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("message", "email", "page_url")
        widgets = {"message": forms.Textarea(attrs={"rows": 3, "maxlength": 2000})}
        labels = {"message": ("Feedback"), "email": ("Email address (optional)")}
