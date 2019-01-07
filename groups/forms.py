from django.forms import ModelForm
from .models import Group

class GroupCreationForm(ModelForm):
    class Meta:
        model = Group
        fields = (
            'name',
            'summary',
        )

'''
'organisers',
'city_or_town', 'country',
'website',
'facebook_group', 'facebook_page',
'official_email', 'lean_email',
'meetup_details', 'meetup_url',
'donations'
'''