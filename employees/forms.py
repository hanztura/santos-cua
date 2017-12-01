from django import forms

from .models import Employee, Salary
from contacts.models import Contact


class EmployeeForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        year_list = list(range(2009, 2019))
        
        model = Employee
        exclude = []
        widgets = {'date_hired': forms.SelectDateWidget(years=year_list)}


class SalaryForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        year_list = list(range(2017, 2025))

        model = Salary
        exclude = []
        widgets = {
        	'date_start': forms.SelectDateWidget(years=year_list),
        	'date_end': forms.SelectDateWidget(years=year_list),
        }

