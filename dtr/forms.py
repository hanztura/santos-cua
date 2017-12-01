from django import forms
from django.contrib.admin import widgets

from .models import Timetable
from contacts.models import Contact


class TimetableForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        model = Timetable
        exclude = []
