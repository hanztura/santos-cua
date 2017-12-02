from django import forms
from django.contrib.admin import widgets

from .models import Holiday


class HolidayForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        model = Holiday
        exclude = []

