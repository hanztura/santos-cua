from django import forms
from django.contrib.admin import widgets

from .models import Issuance, Application


class IssuanceForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        model = Issuance
        exclude = []


class ApplicationForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        model = Application
        exclude = []