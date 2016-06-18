from django_select2 import * # keep above forms import
from django_select2.forms import *
from django import forms
# from django.forms.widgets import CheckboxInput
from bootstrap3_datetime.widgets import DateTimePicker


from .models import Event, Class, Schedule
from accounts.models import Trainee, User
from teams.models import Team
from houses.models import House
from localities.models import Locality
from schedules.constants import WEEKDAYS
from dal import autocomplete

class EventForm(forms.ModelForm):
    weekday = forms.CharField(
        help_text="Which day this event repeats on",
        widget=forms.HiddenInput(),
        required=False,
    )

    day = forms.DateField(
        input_formats=['%m-%d-%Y'],
        widget=DateTimePicker(options={'format': 'MM-DD-YYYY', 'pickTime': False}),
        help_text="Optional to catch one-off days, only happen once", 
        required=False,
    )

    repeating = forms.BooleanField(
        help_text="Check if repeat every week",
        widget=forms.CheckboxInput(),
        required=False,
    )

    schedules = forms.ModelMultipleChoiceField(
        help_text="Which schedule(s) to add the event to",
        queryset=Schedule.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='schedules:schedule-autocomplete'),
        required=False,
    )

    def save(self, commit=True):
        event = super(EventForm, self).save()
        schedules = self.cleaned_data.get('schedules')
        for schedule in schedules:
            schedule.events.add(event)
        event.day = self.cleaned_data.get('day')
        event.weekday = self.cleaned_data.get('weekday')
        event.save()
        return event

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        day = cleaned_data.get('day')
        repeating = cleaned_data.get('repeating')
        if repeating:
            cleaned_data['weekday'] = day.weekday()
            cleaned_data['day'] = None

        # if '7' in weekday and not day:
        #     raise forms.ValidationError(
        #         'Day or weekday is required'
        #     )
        # elif day:
        #     cleaned_data['weekday'] = None

    class Meta:
        model = Event
        fields = ('type', 'name', 'code', 'description', 'class_type', 'monitor', 'start', 'end', 'day')
        help_texts = {
            'start': 'Set the start time of the event',
            'end': 'Set the end time of the event',
        }
        widgets = { 
            'start': DateTimePicker(options={'format': 'HH:mm:ss', 'pickDate': False }),
            'end': DateTimePicker(options={'format': 'HH:mm:ss', 'pickDate': False }),
        }

class ScheduleForm(forms.ModelForm):
    # weekday = forms.ChoiceField(choices=WEEKDAYS, help_text="Which day this event repeats on", initial=7)
    # day = forms.DateField(help_text="Optional to catch one-off days, only happen once", required=False)
    # schedules = forms.ModelMultipleChoiceField(queryset=Schedule.objects.all(), required=False)

    # def save(self, commit=True):
    #     event = super(EventForm, self).save()
    #     schedules = self.cleaned_data.get('schedules')
    #     for schedule in schedules:
    #         schedule.events.add(event)
    #     return event

    # def clean(self):
    #     cleaned_data = super(EventForm, self).clean()
    #     weekday = cleaned_data.get('weekday')
    #     day = cleaned_data.get('day')
    #     # schedules = cleaned_data.get('schedules')
    #     # for schedule in schedules:
    #     #     schedule.events.add(cleaned_data)
    #     #     print 'schedules.events.all()', schedule.events.all()
    #     if '7' in weekday and not day:
    #         raise forms.ValidationError(
    #             'Day or weekday is required'
    #         )
    #     elif day:
    #         cleaned_data['weekday'] = None
    # active_trainees = Trainee.objects.filter(is_active=True)
    # trainees = ModelSelect2MultipleField(queryset=active_trainees, required=False, search_fields=['^first_name', '^last_name'])
    active_trainees = Trainee.objects.filter(is_active=True)
    # trainees = forms.ChoiceField(
    #     required=False,
    #     widget=ModelSelect2MultipleWidget(
    #         queryset=Trainee.objects.filter(is_active=True).order_by('lastname'),
    #         search_fields=['firstname__icontains', 'lastname__icontains'],
    #     )
    # # )
    # trainees = forms.ModelMultipleChoiceField(
    #     queryset=active_trainees.order_by('lastname')
    #     )
    events = forms.ModelMultipleChoiceField(
        queryset=Event.objects.all(),
        )
    class Meta:
        model = Schedule
        fields = ('name', 'comments', 'trainees', 'events', 'priority', 'weeks', 'season', 'import_to_next_term')
        widgets = {
            # 'trainees': autocomplete.ModelSelect2Multiple(
            #                 url='schedules:trainee-autocomplete',
            #                 attrs={
            #                     'data-placeholder': 'Select trainees...',
            #                     'minimum-input-length': 3,
            #                 },
            #             ),
             'trainees': autocomplete.ModelSelect2Multiple(url='schedules:trainee-autocomplete'),
            # 'trainees': ModelSelect2MultipleWidget(
            #     queryset=Trainee.objects.filter(is_active=True).order_by('lastname'),
            #     search_fields=['firstname__icontains', 'lastname__icontains'],
            # )
        }
# class TraineeSelectForm(forms.Form):
#     TERM_CHOICES = ((1, '1'),
#                     (2, '2'),
#                     (3, '3'),
#                     (4, '4'))

#     term = forms.MultipleChoiceField(choices=TERM_CHOICES,
#         widget = forms.CheckboxSelectMultiple,
#         required = False)
#     gender = forms.ChoiceField(choices=User.GENDER,
#         widget = forms.RadioSelect,
#         required = False)
#     hc = forms.BooleanField(required=False, label="House coordinators")
#     team_type = forms.MultipleChoiceField(choices=Team.TEAM_TYPES,
#         widget = forms.CheckboxSelectMultiple,
#         required = False)
#     team = ModelSelect2MultipleField(queryset=Team.objects,
#         required=False,
#         search_fields=['^name'])
#     house = ModelSelect2MultipleField(queryset=House.objects.filter(used=True),
#         required=False,
#         search_fields=['^name'])
#     locality = ModelSelect2MultipleField(queryset=Locality.objects.prefetch_related('city__state'),
#         required=False,
#         search_fields=['^city']) # could add state and country