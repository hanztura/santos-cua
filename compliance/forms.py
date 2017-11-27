from django import forms

from .models import Client, ClientPractitioner, BirCompliance


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

BIRComplianceFormSet = forms.inlineformset_factory(
    Client,
    BirCompliance,
    fields=[
        'bir_form', 'is_active',
    ],
    extra=1,
    can_delete=False,
)