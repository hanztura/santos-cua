from django.db import models
from django.utils import timezone

from contacts.models import Contact
# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)
    resource_persons = models.ManyToManyField(Contact)
    location = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=255, null=True, blank=True)
    cpd_units = models.DecimalField(max_digits=8, decimal_places=2)
    reg_fee = models.DecimalField(max_digits=8, decimal_places=2)


class Schedule(models.Model):
    """docstring for Schedule"""
    event = models.ForeignKey(Event)
    sched_date = models.DateField(timezone.now)
    time_start = models.TimeField(blank=False)
    time_end = models.TimeField(blank=False)
    description = models.CharField(max_length=255)

class Organizer(models.Model):
    """docstring for Organizers"""
    event = models.ForeignKey(Event)
    organizer = models.ForeignKey(Contact)
    role = models.CharField(max_length=20)

class Registration(models.Model):
    """docstring for ClassName"""
    reg_date = models.DateField(default=timezone.now)
    event = models.ForeignKey(Event)
    participant = models.ForeignKey(Contact)
    time_in_1 = models.TimeField(blank=False)
    time_start = models.TimeField(blank=False)
    time_start = models.TimeField(blank=False)
    time_start = models.TimeField(blank=False)
    is_present = models.BooleanField(default=False)
    event_schedule = models.ForeignKey(Schedule , null=True)

class Payment(models.Model):
    """docstring for Payment"""
    pay_type_choices = [
        (1, 'cash'),
        (2, 'check')
    ]

    payor = models.ForeignKey(Contact)
    received_by = models.ForeignKey(Organizer)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    pay_type = models.IntegerField(choices=pay_type_choices)
    check_date = models.DateField()
    check_bank = models.CharField(max_length=10)


class PaymentDetail(models.Model):
    """docstring for PaymentDetail"""
    pay_class_choices = [
        (1, 'Membership Fee'),
        (1, 'Seminar Fee'),
    ]

    payment = models.ForeignKey(Payment)
    pay_class = models.IntegerField(null=True, blank=True, choices=pay_class_choices)
    registration = models.ForeignKey(Registration)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

        