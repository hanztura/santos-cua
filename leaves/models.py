import datetime
from django.db import models
from django.core.validators import MaxValueValidator
from django.utils import timezone

from employees.models import Employee
from public.utils import get_choices_value
# Create your models here.


class Leave():
    leave_choices = (
        (1, "sl"),
        (2, "vl"),
        (3, "sil"),
        (4, "ml"),
        (5, "pyl"),
        (6, "pll"),
    )


class Issuance(models.Model):
    valid_onyear_choices = [
        (2017,2017),
        (2018,2018),
    ]

    leave = models.IntegerField(choices=Leave.leave_choices)
    date = models.DateField(default=datetime.date.today)
    employee = models.ForeignKey(Employee)
    hours = models.PositiveIntegerField(default=0)
    valid_on_year = models.IntegerField(null=True, choices=valid_onyear_choices)
    remarks = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return ' | '.join([self.employee.contact.full_name, str(self.leave), str(self.hours)])

    @property
    def get_leave(self):
        return get_choices_value(Leave.leave_choices, self.leave)

class Application(models.Model):
    leave = models.IntegerField(choices=Leave.leave_choices)
    employee = models.ForeignKey(Employee)
    date = models.DateField()
    remarks = models.CharField(max_length=100, null=True, blank=True)
    charge_to_issuances = models.BooleanField(default=True)
    paid_hours = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(24),])

    def __str__(self):
        return ' | '.join([self.employee.contact.full_name, str(self.leave), str(self.date) , str(self.paid_hours)])

    @property
    def get_leave(self):
        return get_choices_value(Leave.leave_choices, self.leave)

    # @property
    # def get_available_leavecredits(self):
    #     ret = 0
    #     issuances = Issuance.objects.filter(leave=self.leave, valid_on_year=date.year)
    #     issuances_hours = leave_issuances.aggregate(models.Sum('hours'))['hours__sum']

    #     applications = Application.objects.filter(leave=self.leave, date__year=date.year).exclude()
    #     return ret