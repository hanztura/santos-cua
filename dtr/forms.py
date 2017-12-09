from django import forms
from django.contrib.admin import widgets

from .models import Timetable, Schedule, ScheduleTimetable, Log, Attendance, AttendanceLog, GraceLateIn
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


class LogForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        model = Log
        exclude = []


class AttendanceForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        model = Attendance
        exclude = []


class GraceLateInForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        model = GraceLateIn
        exclude = []


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
    exclude = ('schedule', 'work'),
    labels = {
        'minutes_threshold_early_in': 'early in',
        'minutes_threshold_late_in': 'late in',
        'minutes_threshold_early_out': 'early out',
        'minutes_threshold_late_out': 'late out',
        'sub_project': 'project/sub-project'
    },
    extra=1,
)

AttendanceLogFormSet = forms.inlineformset_factory(
    Attendance,
    AttendanceLog,
    exclude = ('attendance', ),
    labels = {
        'schedule_timetable': 'timetable',
        'final_date_time_in': 'in',
        'final_date_time_out': 'out',
        'minutes_late_in': 'late in',
        'minutes_early_out': 'early out',
        'minutes_night_premium': 'nigth',
        'minutes_ot_premium': 'ot',
    },
    extra=1,
)


class ProcessDTRForm(forms.Form):
    employee_id =  forms.IntegerField()

ProcessDTRFormset = forms.formset_factory(ProcessDTRForm, extra=2)