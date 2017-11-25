from django import forms

from .models import Employee
from contacts.models import Contact


class EmployeeForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        year_list = list(range(2009, 2019))
        
        model = Employee
        exclude = []
        widgets = {'date_hired': forms.SelectDateWidget(years=year_list)}

