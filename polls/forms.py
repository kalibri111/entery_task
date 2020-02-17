from django import forms
from .models import *
from crispy_forms.helper import FormHelper


class PoolChoiceForm(forms.Form):
    choices = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': '  custom-checkbox', 'type': 'checkbox'}),
        label='',
        help_text=None
    )

    @staticmethod
    def question_constructor(question):
        inst = PoolChoiceForm()
        inst.fields['choices'] = forms.MultipleChoiceField(
            choices=[(obj, obj) for obj in Choice.objects.filter(question__exact=question)],
            widget=forms.CheckboxSelectMultiple(attrs={'class': '  custom-checkbox', 'type': 'checkbox'}))
        return inst

    @staticmethod
    def bound_constructor(question, request):
        inst = PoolChoiceForm(request)
        inst.fields['choices'] = forms.MultipleChoiceField(
            choices=[(obj, obj) for obj in Choice.objects.filter(question__exact=question)],
            widget=forms.CheckboxSelectMultiple(attrs={'class': '  custom-checkbox', 'type': 'checkbox'}))
        return inst
