from django import forms
from .models import Discipline, Summary
from accounts.models import Trainee
from houses.models import House



class NewDisciplineForm(forms.ModelForm):

    class Meta:
        model = Discipline

    def save(self, commit=True):
        discipline = super(NewDisciplineForm, self).save(commit=False)
        if commit:
            discipline.save()
        return discipline


class NewSummaryForm(forms.ModelForm):

    class Meta:
        model = Summary
        exclude = ('approved', 'discipline',)

    def save(self, commit=True):
        summary = super(NewSummaryForm, self).save(commit=False)
        if commit:
            summary.save()
        return summary


class EditSummaryForm(forms.ModelForm):

    class Meta:
        model = Summary
        exclude = ('book', 'chapter', 'discipline', 'approved', )

    def save(self, commit=True):
        summary = super(EditSummaryForm, self).save(commit=False)
        if commit:
            summary.save()
        return summary


class HouseDisciplineForm(forms.ModelForm):

    class Meta:
        model = Discipline
        exclude = ('trainee',)
    House = forms.ModelChoiceField(House.objects)
