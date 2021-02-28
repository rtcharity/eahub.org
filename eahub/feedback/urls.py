from django.urls import path

from . import views

app_name = "feedback"
urlpatterns = [path("submit/", views.ajax_post_view, name="submit_feedback")]
