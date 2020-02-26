from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from crispy_forms.bootstrap import FormActions, StrictButton, Div


class PoolChoiceForm(forms.Form):
    choices = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple(attrs={'class': '  custom-checkbox', 'type': 'checkbox'}), label=False)

    def __init__(self, data=None, *args, **kwargs):
        super(PoolChoiceForm, self).__init__(data)
        self.fields['choices'].choices = Choice.objects.filter(question__exact=kwargs['question']). \
            values_list('choice_text', 'choice_text')
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_class = 'form-check'
        self.helper.form_id = 'some_id'
        self.helper.layout = Layout(
            Fieldset(
                None,
                'choices'
            ),
            FormActions(
                StrictButton('Голосовать', css_class='btn-success', type='Submit')
            )
        )
