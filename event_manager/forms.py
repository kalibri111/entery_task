from django import forms
from django.core.exceptions import ValidationError


class SearchForm(forms.Form):
    field = forms.CharField(widget=forms.TextInput)
