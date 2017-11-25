from django.db import models

# Create your models here.


class Rdo(models.Model):
    """docstring for ClassName"""
    code = models.CharField(max_length=3, blank=True)
    rdo = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.code


class BirForm(models.Model):
    """docstring for ClassName"""
    dpc_choices = [
        (1, 'monthly'),
        (2, 'quarterly'),
        (3, 'annually'),
        (4, 'custom'),
    ]

    dcr_choices = [
        (1, 'absolute'),
        (2, 'relative'),
    ]

    ddt_choices = [
        (1, 'fix'),
        (2, 'count'),
    ]

    form_code = models.CharField(max_length=10, null=False, blank=False, verbose_name='code')
    form = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=250, null=True, blank=True)
    deadline_period = models.IntegerField(choices=dpc_choices, verbose_name='period', )
    deadline_cy_ref = models.IntegerField(choices=dcr_choices, verbose_name='bus. year ref', default=2)
    deadline_date_type = models.IntegerField(choices=ddt_choices, verbose_name='date type', default=1)

    def __str__(self):
        ret = str(self.form_code)
        return ret

    @property
    def dead_period(self):
        ret = self.deadline_period
        # get string value
        for choice in self.dpc_choices:
            if choice[0] == ret:
                ret = choice[1][0].upper()
                break

        return ret

    @property
    def dead_by_ref(self):
        ret = self.deadline_cy_ref
        # get string value
        for choice in self.dcr_choices:
            if choice[0] == ret:
                ret = choice[1][0].upper()
                break

        return ret

    @property
    def dead_date_type(self):
        ret = self.deadline_date_type
        # get string value
        for choice in self.ddt_choices:
            if choice[0] == ret:
                ret = choice[1][0].upper()
                break

        return ret


class BirFormSchedule(models.Model):
    """docstring for ClassName"""
    bir_form = models.ForeignKey(BirForm, related_name='schedules')
    index = models.IntegerField(null=False, blank=False)
    month = models.IntegerField(null=False, blank=False)
    day = models.IntegerField(null=False, blank=False)
