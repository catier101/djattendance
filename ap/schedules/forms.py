from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from django_select2 import *

from .models import Event
from accounts.models import Trainee, User
from teams.models import Team
from houses.models import House
from localities.models import Locality


class EventForm(forms.ModelForm):
    trainees = ModelSelect2MultipleField(queryset=Trainee.objects, required=False, search_fields=['^first_name', '^last_name'])

    class Meta:
        model = Event
        fields = ('type', 'name', 'code', 'description', 'classs', 'monitor', 'term', 'start', 'end')
        widgets = { 'start': DateTimePicker(options={'format': 'MM/DD/YYYY HH:mm'}),
                    'end': DateTimePicker(options={'format': 'MM/DD/YYYY HH:mm'}) }


class TraineeSelectForm(forms.Form):
    TERM_CHOICES = ((1, '1'),
                    (2, '2'),
                    (3, '3'),
                    (4, '4'))

    term = forms.MultipleChoiceField(choices=TERM_CHOICES, 
        widget = forms.CheckboxSelectMultiple,
        required = False)
    gender = forms.ChoiceField(choices=User.GENDER,
        widget = forms.RadioSelect,
        required = False)
    hc = forms.BooleanField(required=False, label="House coordinators")
    team_type = forms.MultipleChoiceField(choices=Team.TEAM_TYPES, 
        widget = forms.CheckboxSelectMultiple,
        required = False)
    team = ModelSelect2MultipleField(queryset=Team.objects, 
        required=False, 
        search_fields=['^name'])
    house = ModelSelect2MultipleField(queryset=House.objects.filter(used=True), 
        required=False, 
        search_fields=['^name'])
    locality = ModelSelect2MultipleField(queryset=Locality.objects,
        required=False,
        search_fields=['^city']) # could add state and country

