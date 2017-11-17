from django import forms

from .models import Contact, Phone, Address, Email


class ContactForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        year_list = list(range(1950, 2017))
        
        model = Contact
        exclude = ['is_deleted']
        widgets = {'date_of_birth': forms.SelectDateWidget(years=year_list)}


PhoneFormSet = forms.inlineformset_factory(
    Contact,
    Phone,
    fields=[
        'phone_type', 'number', 'person', 'is_active'
    ],
    extra=1,
)

AddressFormSet = forms.inlineformset_factory(
    Contact,
    Address,
    fields=[
        'address', 'bldg', 'streets', 'town', 'city'
    ],
    extra=1,
)

EmailFormSet = forms.inlineformset_factory(
    Contact,
    Email,
    fields=[
        'email', 'person', 'is_active',
    ],
    extra=1,
)