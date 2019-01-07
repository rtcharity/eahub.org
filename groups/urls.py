from django.urls import path
from . import views

urlpatterns = [
    path('<int:group_id>', views.view_group, name='group'),
    path('create', views.create_group, name='create_group'),
]
