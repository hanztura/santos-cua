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
    leave = models.IntegerField(choices=Leave.leave_choices)
    employee = models.ForeignKey(Employee)
    hours = models.PositiveIntegerField(default=0)
    valid_from_date = models.DateField(default=timezone.now,verbose_name='From')
    valid_until_date = models.DateField(verbose_name='Until')
    remarks = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return ' | '.join([self.employee.contact.full_name, self.leave, self.hours])

    @property
    def get_leave(self):
        return get_choices_value(Leave.leave_choices, self.leave)

class Application(models.Model):
    leave = models.IntegerField(choices=Leave.leave_choices)
    employee = models.ForeignKey(Employee)
    date = models.DateField()
    hours = models.PositiveIntegerField(default=8, validators=[MaxValueValidator(24),])
    remarks = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return ' | '.join([self.employee.contact.full_name, str(self.leave), str(self.date) , str(self.hours)])

    @property
    def get_leave(self):
        return get_choices_value(Leave.leave_choices, self.leave)