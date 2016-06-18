from django.forms import Form, ModelForm, formset_factory
from django.forms import CharField, Textarea, TextInput, MultipleChoiceField
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django_select2 import *
from django_select2.forms import *

from .models import Trainee, Exam, Section

class TraineeSelectForm(Form):
    trainees = MultipleChoiceField(
        required=False,
        widget=ModelSelect2MultipleWidget(
            model=Trainee,
            search_fields=['firstname__icontains', 'lastname__icontains']
        )
    )
class ExamCreateForm(ModelForm):
    class Meta:
        model = Exam
        fields = ('training_class', 'name', 'is_open', 'duration', 'category')