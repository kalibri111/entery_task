from django import forms
from django.core.exceptions import ValidationError


class SearchForm(forms.Form):
    field = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mr-sm-2',
                                                          'placeholder': 'Поиск', 'aria-label': 'Search'}))
