from django.forms import ModelForm
from .models import Group

class CreateGroupForm(ModelForm):
    class Meta:
        model = Group
        fields = (
            'name',
            'summary',
            #'organisers',
            'city_or_town', 'country',
            'website',
            'facebook_group', 'facebook_page',
            'official_email',
            'meetup_details', 'meetup_url',
            'lat', 'lon',
            #'donations'
        )

class EditGroupForm(ModelForm):
    class Meta:
        model = Group
        fields = (
            'name', 'group_type', 'summary',
            'total_group_donations',
            'city_or_town', 'country',
            'website',
            'facebook_group', 'facebook_page',
            'official_email',
            'meetup_details', 'meetups_per_month', 'meetup_url',
            'lat', 'lon',
            # TODO: add organisers & donations fields
        )