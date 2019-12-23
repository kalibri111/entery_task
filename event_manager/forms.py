from django import forms
from .models import User, Member


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class MemberForm(forms.Form):
    submit = forms.CheckboxInput()
