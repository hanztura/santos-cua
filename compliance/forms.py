from django import forms

from .models import Client


class ClientForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        year_list = list(range(2009, 2031))
        
        model = Client
        exclude = ['is_deleted']
        widgets = {
            'date_start': forms.SelectDateWidget(years=year_list),
            'date_end': forms.SelectDateWidget(years=year_list),
        }

