from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Profile
from .forms import ProfileCreationForm, ProfileChangeForm

@admin.register(Profile)
class UserAdmin(UserAdmin):
    model = Profile
    add_form = ProfileCreationForm
    form = ProfileChangeForm
    list_display = ('id', 'first_name', 'last_name', 'email')
    
    exclude = ('username',)
    fieldsets = (
        ('Personal info', {'fields': (
            'first_name', 'last_name', 'email', 'password',
            'country', 'city_or_town'
        )}),
        ('Stats', {'fields': (
            'last_login', 'date_joined',
            'is_active', 'is_staff', 'is_superuser'
        )}),
    )
    readonly_fields = ('last_login', 'date_joined')