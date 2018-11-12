from django.contrib import admin

from .models import Profile, Group

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'lat', 'lon')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name','lat', 'lon')