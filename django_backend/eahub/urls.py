from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profiles/', views.profiles, name='profiles'),
    path('groups/', views.groups, name='groups'),
    path('admin/', admin.site.urls),
]