from django import forms
from .models import User, Trainee

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('firstname', 'lastname',)


class EmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
