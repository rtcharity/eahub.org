from django.views.generic.edit import CreateView

from eahub.feedback.models import Feedback


class FeedbackCreate(CreateView):
    model = Feedback
    fields = ["message", "email", "page_url"]
    success_url = "/"
