from django.db import models
from django.utils import timezone

from bir.models import Rdo, BirForm
from contacts.models import Contact
from employees.models import Employee


from django.utils import timezone
# Create your models here.


class Client(models.Model):

    line_of_business_choices = [
        (1, 'OTHER TELECOMMUNICATION'),
        (2, 'OTHER WHOLESALING'),
        (3, 'SALE OF AGGREGATES'),
        (4, 'OTHER RETAIL SALE IN SPECIALIZED STORES'),
    ]

    engagement_series_num = models.IntegerField(null=True, blank=True, editable=False)
    contact = models.ForeignKey(Contact, verbose_name='client')
    rdo = models.ForeignKey(Rdo)
    line_of_business = models.IntegerField(
        null=True,
        blank=True,
        choices=line_of_business_choices
    )
    date_start = models.DateField(
        default=timezone.now,
        null=False,
        blank=False,
    )
    date_end = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(null=False, default=False)
    is_deleted = models.BooleanField(default=False)
    practitioners = models.ManyToManyField(
        Employee,
        through='ClientPractitioner'
    )

    def __str__(self):
        ret = self.contact.alias
        return ret

    @property
    def lob(self):
        _lob = self.line_of_business
        if (not _lob):
            return '-'
            
        for k,v in self.line_of_business_choices:
            if (_lob == k):
                return v
                break
            continue

        return '-'

    @property
    def doc_ref(self):
        if (not ((self.engagement_series_num == None) or (self.date_start == None))):
            series = self.engagement_series_num
            year = str(self.date_start.year)
            prefix = 'EC'

            # add trailing zeroes to series
            series = str(100000 + series)[1:]

            ret = '-'.join([prefix, year,series])

        else:
            ret = '---'

        return ret
    @property
    def assigned(self):
        ret = '---'
        if (self.practitioners):
            ret = self.practitioners.first()
        return ret


class ClientPractitioner(models.Model):
    """docstring for ClientPractitioner"""
    class Meta:
        verbose_name = 'Practitioner'
        ordering = ['-date_assigned',]
            
    client = models.ForeignKey(Client)
    employee = models.ForeignKey(Employee)
    date_assigned = models.DateField(
        null=False,
        blank=False,
    )
    date_transferred = models.DateField(
        null=True,
        blank=True,
    )
    remarks = models.CharField(max_length=100, null=True, blank=True)


class BirCompliance(models.Model):
    """docstring for ClassName"""
    class Meta:
        verbose_name_plural = 'Compliance - BIR'

    client = models.ForeignKey(Client)
    bir_form = models.ForeignKey(BirForm)
    is_active = models.BooleanField(null=False, default=False)

    def __str__(self):
        ret = str(self.client.contact.alias) + ' | ' + str(self.bir_form.form_code)
        return ret


class BirDeadline(models.Model):
    """docstring for ClassName"""
    class Meta:
        verbose_name_plural = 'Deadlines - BIR'


    compliance = models.ForeignKey(BirCompliance)
    date_deadline = models.DateField(null=False, blank=False, default=timezone.now, verbose_name='deadline')
    date_notify_start = models.DateField(null=False, blank=False, verbose_name='notification starts on')

    def __str__(self):
        ret = ' | '.join([str(self.compliance), str(self.date_deadline)])
        return ret


class DeadlineStatus(models.Model):
    """docstring for ClassName"""


    class Meta:
        verbose_name_plural = 'Deadline Status'
    

    status_choices = [
        (1, 'Working'),
        (2, 'Drafted'),
        (3, 'Filing'),
        (4, 'Verification'),
        (5, 'Paid'),
        (6, 'Done'),
    ]

    bir_deadline = models.ForeignKey(BirDeadline)
    status = models.IntegerField(
        null=False,
        blank=False,
        default=1,
        choices=status_choices
    )
    as_of = models.DateTimeField(default=timezone.now, null=False,)
    remarks = models.CharField(max_length=100, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    @property
    def get_client(self):
        ret = str(self.bir_deadline.compliance.client)
        return ret

    @property
    def get_status_verbose(self):
        status = self.status
        if (not status):
            return '-'
            
        for k,v in self.status_choices:
            if (status == k):
                return v
                break
            continue

        return '-'

