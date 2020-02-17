from django import forms
from .models import *


class PoolChoiceForm(forms.Form):
    choices = forms.MultipleChoiceField(
            choices=[],
            widget=forms.CheckboxSelectMultiple(attrs={'class': '  custom-checkbox', 'type': 'checkbox'}))

    def __init__(self, data=None, *args, **kwargs):
        super(PoolChoiceForm, self).__init__(data)
        self.fields['choices'].choices = Choice.objects.filter(question__exact=kwargs['question']).values_list('choice_text', 'choice_text')
