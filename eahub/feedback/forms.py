from django.forms import ModelForm

from eahub.feedback.models import Feedback


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ["message", "email", "page_url"]
