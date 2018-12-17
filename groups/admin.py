from django.contrib import admin

from .models import Group

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','country', 'city_or_town')