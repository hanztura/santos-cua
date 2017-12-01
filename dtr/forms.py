from django import forms
from django.contrib.admin import widgets

from .models import Timetable, Schedule, ScheduleTimetable
from contacts.models import Contact


class TimetableForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        model = Timetable
        exclude = []


class ScheduleForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        model = Schedule
        exclude = ['timetables']


# class ScheduleTimetableForm(forms.ModelForm):
#     """docstring for ContactForm"""
#     class Meta:
#         model = ScheduleTimetable
#         exclude = ['schedule']


# ScheduleTimetableFormSet = forms.formset_factory(
#     ScheduleTimetableForm,
#     extra=1,
# )

ScheduleTimetableFormSet = forms.inlineformset_factory(
    Schedule,
    ScheduleTimetable,
    exclude = ('schedule', 'sub_project', 'work'),
    labels = {
        'minutes_threshold_early_in': 'early in',
        'minutes_threshold_late_in': 'late in',
        'minutes_threshold_early_out': 'early out',
        'minutes_threshold_late_out': 'late out',
    },
    extra=1,
)
