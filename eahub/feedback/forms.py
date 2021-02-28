from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("message", "email", "page_url")
        widgets = {
            "message": forms.Textarea(
                attrs={"rows": 3, "maxlength": 5000, "required": "true"}
            )
        }
        labels = {"message": ("Feedback"), "email": ("Email address (optional)")}
