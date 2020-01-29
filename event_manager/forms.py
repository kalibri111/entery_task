from django import forms
from django.core.exceptions import ValidationError


class FilterForm(forms.Form):
    since = forms.DateField(widget=forms.DateInput, help_text='Since')
    to = forms.DateField(widget=forms.DateInput, help_text='To')

    def clean_since(self):
        since = self.cleaned_data['since']
        to = self.cleaned_data['to']
        if to and since > to:
            raise ValidationError('Since date bigger than To')
        return since

    def clean_to(self):
        since = self.cleaned_data['since']
        to = self.cleaned_data['to']
        if since and to < since:
            raise ValidationError('To date smaller than Since')
        return since
