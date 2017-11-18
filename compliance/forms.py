from django import forms

from .models import Client, ClientPractitioner


class ClientForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        year_list = list(range(2009, 2031))
        
        model = Client
        exclude = ['practitioners']
        widgets = {
            'date_start': forms.SelectDateWidget(years=year_list),
            'date_end': forms.SelectDateWidget(years=year_list),
        }


PractitionerFormSet = forms.inlineformset_factory(
    Client,
    ClientPractitioner,
    fields=[
        'employee', 'date_assigned', 'date_transferred', 'remarks'
    ],
    extra=1,
)