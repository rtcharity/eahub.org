from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import Feedback
from .forms import FeedbackForm


def submit_feedback(request):
    if request.method == "POST":
        url = request.path
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.page_url = url
            form.save()
            return HttpResponseRedirect("/profiles")
        else:
            form = FeedbackForm()
            return HttpResponse()
            # display message saying it wasn't valid
