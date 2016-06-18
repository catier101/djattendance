from django.forms import Form, ModelForm, formset_factory
from django.forms import CharField, Textarea, TextInput
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django_select2 import ModelSelect2MultipleField

from .models import Trainee, Exam, Section

class TraineeSelectForm(Form):
    trainees = ModelSelect2MultipleField(queryset=Trainee.objects, 
                                         required=False, 
                                         search_fields=['^first_name', '^last_name'])

class ExamCreateForm(ModelForm):
    class Meta:
        model = Exam
        fields = ('training_class', 'name', 'is_open', 'duration', 'category')