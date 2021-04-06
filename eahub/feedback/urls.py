from django.urls import path

from eahub.feedback import views

app_name = "feedback"
urlpatterns = [path("submit/", views.FeedbackCreate.as_view(), name="submit_feedback")]
