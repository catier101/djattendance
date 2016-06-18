from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from django_select2 import *

from .models import Event, Class, Schedule
from accounts.models import Trainee, User
from teams.models import Team
from houses.models import House
from localities.models import Locality
from schedules.constants import WEEKDAYS


class EventForm(forms.ModelForm):
    active_trainees = Trainee.objects.select_related().filter(is_active=True)
    trainees = ModelSelect2MultipleField(queryset=active_trainees, required=False, search_fields=['^first_name', '^last_name'])

    class Meta:
        model = Event
        fields = ('type', 'name', 'code', 'description', 'monitor', 'start', 'end', 'day', 'weekday')
        widgets = { 'start': DateTimePicker(options={'format': 'MM/DD/YYYY HH:mm'}),
                    'end': DateTimePicker(options={'format': 'MM/DD/YYYY HH:mm'}) }

    repeat = forms.MultipleChoiceField(choices=WEEKDAYS, help_text="Which days this event repeats on")
    duration = forms.IntegerField(help_text="How many weeks this event repeats for")
    active_trainees = Trainee.objects.filter(is_active=True)
    trainees = ModelSelect2MultipleField(queryset=active_trainees, required=False, search_fields=['^first_name', '^last_name'])

    class Meta:
        model = Event
        fields = ('type', 'name', 'code', 'description', 'monitor', 'start', 'end', 'day', 'weekday')
        help_texts = {
            'start': 'Set the date to the first occurrence of the event',
            'end': 'Set the date to the first occurrence of the event',
        }
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
    locality = ModelSelect2MultipleField(queryset=Locality.objects.prefetch_related('city__state'),
        required=False,
        search_fields=['^city']) # could add state and country

