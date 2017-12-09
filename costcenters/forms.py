from django import forms

from .models import Branch, Project, Work, Holiday
from contacts.models import Contact


class BranchForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        model = Branch
        exclude = []


class ProjectForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        model = Project
        exclude = []


class WorkForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        model = Work
        exclude = []


class HolidayForm(forms.ModelForm):
    """docstring for ContactForm"""
    class Meta:
        model = Holiday
        exclude = []

