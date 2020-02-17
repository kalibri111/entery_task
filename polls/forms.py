from django import forms
from .models import *
from crispy_forms.helper import FormHelper


class PoolChoiceForm(forms.Form):
    choices = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': '  custom-checkbox', 'type': 'checkbox'}),
        label='',
        help_text=None
    )

    def __init__(self, data=None, *args, **kwargs):
        super(PoolChoiceForm, self).__init__(data)
        self.fields['choices'] = forms.MultipleChoiceField(
            choices=[(obj, obj) for obj in Choice.objects.filter(question__exact=kwargs['question'])],
            widget=forms.CheckboxSelectMultiple(attrs={'class': '  custom-checkbox', 'type': 'checkbox'}))
