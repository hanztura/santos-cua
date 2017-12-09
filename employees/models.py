import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from contacts.models import Contact

# Create your models here.

class Employee(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, verbose_name='Name')
    id_num = models.CharField(max_length=30, unique=True, null=True, blank=True)
    abbr = models.CharField(max_length=5, unique=True, null=True, blank=True)
    date_hired = models.DateField(default=timezone.now)
    date_resigned = models.DateField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    # 2017-11-29
    user = models.OneToOneField(User, null=True, related_name='employee')
    supervisors = models.ForeignKey('self', null=True, related_name='sups')

    def __str__(self):
        # employees full name
        return self.contact.full_name

    @property
    def is_resigned(self, verbose_name='resigned'):
        ret = False
        return ret


class Salary(models.Model):

    payroll_type_choices = [
        (1, 'Daily'),
        (2, 'Periodic'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Name', related_name='salaries')
    date_start = models.DateField(default=timezone.now)
    date_end = models.DateField(null=True, blank=True)
    payroll_type = models.IntegerField(
        default = 2,
        choices=payroll_type_choices,
    )
    # monthly_work_days_ave = models.IntegerField(default=26)
    monthly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def get_payroll_type(self):
        for payroll_type in self.payroll_type_choices:
            if payroll_type[0] == self.payroll_type:
                ret = payroll_type[1]
                break
        return ret