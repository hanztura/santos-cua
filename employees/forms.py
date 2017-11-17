from django import forms

from .models import Employee
from contacts.models import Contact


class EmployeeForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        year_list = list(range(2009, 2017))
        
        model = Employee
        exclude = ['is_deleted']
        widgets = {'date_hired': forms.SelectDateWidget(years=year_list)}

