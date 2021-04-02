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
        # todo: replace with CreateView
        labels = {"message": ("Feedback"), "email": ("Email address (optional)")}
