from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import ProfileCreationForm, ProfileChangeForm
from .models import Profile

class ProfileAdmin(UserAdmin):
    model = Profile
    add_form = ProfileCreationForm
    form = ProfileChangeForm
    list_display = ('email', 'first_name', 'last_name')

admin.site.register(Profile, ProfileAdmin)