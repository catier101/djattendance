from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from .models import Discipline, Summary
from accounts.models import Trainee, Statistics
from houses.models import House
from books.models import Book



class NewDisciplineForm(forms.ModelForm):
    class Meta:
        model = Discipline
        fields = '__all__'
        widgets = { 'due': DateTimePicker(options={'format': 'MM/DD/YYYY'}) }

    def save(self, commit=True):
        discipline = super(NewDisciplineForm, self).save(commit=False)
        if commit:
            discipline.save()
        return discipline


class NewSummaryForm(forms.ModelForm):

    class Meta:
        model = Summary
        exclude = ('approved', 'discipline', 'deleted', 'fellowship', 'hard_copy')
        widgets = {'minimum_words': forms.HiddenInput()}
        
    def __init__(self, *args, **kwargs):
        t = kwargs.pop('trainee', None)
        super(NewSummaryForm, self).__init__(*args, **kwargs)

        # Auto-populate from last lifestudy book + chapter
        s = Statistics.objects.filter(trainee=t).count()
        # Test to see if statistics exists currently for user
        if s:
            (book_id, chpt) = t.statistics.latest_ls_chpt.split(':')
            self.initial['book'] = Book.objects.get(id=book_id)
            self.initial['chapter'] = int(chpt) + 1

    def save(self, commit=True):
        summary = super(NewSummaryForm, self).save(commit=False)
        if commit:
            #update the last book for discipline for trainee
            t = summary.discipline.trainee
            stat_str = str(summary.book.id) + ':' + str(summary.chapter)
            # Update or create for the first time new statistics
            Statistics.objects.update_or_create(trainee=t, defaults={'latest_ls_chpt': stat_str})
            summary.save()
        return summary


class EditSummaryForm(forms.ModelForm):

    class Meta:
        model = Summary
        exclude = ('book', 'chapter', 'discipline', 'approved', 'deleted', 'fellowship', 'hard_copy')
        widgets = {'minimum_words': forms.HiddenInput()}

    def save(self, commit=True):
        summary = super(EditSummaryForm, self).save(commit=False)
        if commit:
            summary.save()
        return summary


class HouseDisciplineForm(forms.ModelForm):

    class Meta:
        model = Discipline
        exclude = ('trainee',)
        widgets = { 'due': DateTimePicker(options={'format': 'MM/DD/YYYY'}) }
        
    House = forms.ModelChoiceField(House.objects)