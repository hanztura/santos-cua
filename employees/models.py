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
    user = models.OneToOneField(User, null=True, related_name='user')
    supervisors = models.ForeignKey('self', null=True, related_name='sups')

    def __str__(self):
        # employees full name
        return self.contact.full_name

    @property
    def is_resigned(self, verbose_name='resigned'):
        ret = False
        return ret
