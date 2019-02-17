from django.forms import ModelForm
from .models import Group

class CreateGroupForm(ModelForm):
    class Meta:
        model = Group
        fields = (
            'name', 'summary',
            'group_type', 'group_type_other',
            'city_or_town', 'country',
            'email' , 'website',
            'facebook_group', 'facebook_page',
            'meetup_details', 'meetups_per_month', 'meetup_url',
        )

class EditGroupForm(ModelForm):
    class Meta:
        model = Group
        fields = (
            'name', 'summary',
            'group_type', 'group_type_other',
            'city_or_town', 'country',
            'email' , 'website',
            'facebook_group', 'facebook_page',
            'meetup_details', 'meetups_per_month', 'meetup_url',
        )