from django import forms
from .models import *


class PoolChoiceForm(forms.Form):
    choices = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple
    )

    @staticmethod
    def question_constructor(question):
        inst = PoolChoiceForm()
        inst.fields['choices'] = forms.MultipleChoiceField(
            choices=[(obj, obj) for obj in Choice.objects.filter(question__exact=question)],
            widget=forms.CheckboxSelectMultiple)
        return inst

    @staticmethod
    def bound_constructor(question, request):
        inst = PoolChoiceForm(request)
        inst.fields['choices'] = forms.MultipleChoiceField(
            choices=[(obj, obj) for obj in Choice.objects.filter(question__exact=question)],
            widget=forms.CheckboxSelectMultiple)
        return inst
