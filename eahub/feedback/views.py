from django.http import HttpResponse, JsonResponse

from .forms import FeedbackForm
from .models import Feedback


def ajax_post_view(request):
    model = Feedback
    form_class = FeedbackForm
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            #todo: replace with CreateView
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=418)
