from datetime import datetime, timedelta
from django import forms
from django.db import models
from django.utils import timezone

from costcenters.models import Project, Work
from employees.models import Employee
from leaves.models import Application
from public.utils import get_choices_value

# Create your models here.
class GraceLateIn(models.Model):


	grace_type_choices = (
		(1, 'instance'),
		(2, 'periodic'),
	)
	grace_subtype_choices = (
		(1, 'daily'),
		(2, 'monthly'),
	)
	value_type_choices = (
		(1, 'simple'),
		(2, 'complex'),
	)

	grace_type = models.IntegerField(default=1, choices=grace_type_choices)
	grace_sub_type = models.IntegerField(null=True, blank=True, choices=grace_subtype_choices, default=None)
	value_minutes = models.IntegerField(default=0,)
	value_type = models.IntegerField(default=1, choices=value_type_choices)
	alias = models.CharField(max_length=20)
	remarks = models.CharField(max_length=100, null=True, blank=True)

	@property
	def get_grace_type(self):
		ret = get_choices_value(self.grace_type_choices, self.grace_type)
		return ret

	@property
	def get_grace_subtype(self):
		ret = get_choices_value(self.grace_subtype_choices, self.grace_sub_type)
		return ret	

	def __str__(self):
		ret = ' | '.join([str(self.alias), str(self.get_grace_type), str(self.value_minutes)])
		return ret


class Timetable(models.Model):

	is_rest_day = models.BooleanField(default=False)
	time_in = models.TimeField('In', null=True, blank=True)
	time_out = models.TimeField('Out', null=True, blank=True)
	is_timein_nextday = models.BooleanField(default=False)
	is_timeout_nextday = models.BooleanField(default=False)
	hours_npb = models.DecimalField('Non-paid Break', null=True, max_digits=4, decimal_places=2, blank=True)
	hours_scheduled = models.DecimalField('Scheduled', null=True, max_digits=4, decimal_places=2, blank=True)
	hours_paid = models.DecimalField('Paid', null=True, max_digits=4, decimal_places=2, blank=True)
	remarks = models.CharField(max_length=100, null=True, blank=True)
	is_ot = models.BooleanField(default=False, verbose_name='OT')
	grace_late_in = models.ForeignKey(GraceLateIn, null=True, blank=True)

	def __str__(self):
		ret = str(self.remarks) + ' | ' + 'IN: ' + str(self.time_in) + ' OUT: ' + str(self.time_out)
		
		if self.is_ot:
			ret = '(OVERTIME) ' + ret

		return ret


class Schedule(models.Model):


	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	date = models.DateField()
	is_rest_day = models.BooleanField(default=False)
	remarks	= models.CharField(max_length=100, null=True, blank=True)
	# timetables = models.ManyToManyField(Timetable, through='ScheduleTimetable')

	def __str__(self):
		return self.employee.contact.full_name


class ScheduleTimetable(models.Model):


	schedule = models.ForeignKey(Schedule)
	timetable = models.ForeignKey(Timetable)
	minutes_threshold_early_in = models.IntegerField(default=0, blank=True)
	minutes_threshold_late_in = models.IntegerField(default=0, blank=True)
	minutes_threshold_early_out = models.IntegerField(default=0, blank=True)
	minutes_threshold_late_out = models.IntegerField(default=0, blank=True)
	sub_project = models.ForeignKey(Project, verbose_name='Project', null=True, blank=True)
	work = models.ForeignKey(Work, verbose_name='Scope of work', null=True, blank=True)

	def __str__(self):
		return ' | '.join([str(self.schedule.employee), str(self.schedule.date) ,str(self.timetable)])

	@property
	def get_datetime_inout(self):
		ret = {}
		date = self.schedule.date
		datetime_in = None
		datetime_out = None
		if not self.timetable.is_rest_day:
			time_in = self.timetable.time_in
			time_out = self.timetable.time_out
			datetime_in = datetime(year=date.year, month=date.month, day=date.day) + timedelta(hours=time_in.hour, minutes=time_in.minute)
			datetime_out = datetime(year=date.year, month=date.month, day=date.day) + timedelta(hours=time_out.hour, minutes=time_out.minute)
			if self.timetable.is_timein_nextday:
				datetime_in = datetime_in + timedelta(hours=24)
				datetime_out = datetime_out + timedelta(hours=24)
			elif self.timetable.is_timeout_nextday:
				datetime_out = datetime_out + timedelta(hours=24)
			else:
				pass
		
		ret['in'] = datetime_in
		ret['out'] = datetime_out
		return ret


class Log(models.Model):


	log_type_choices = [
		(1, 'None'),
		(2, 'In'),
		(3, 'Out'),
		(4, 'Overtime - In'),
		(5, 'Overtime - Out'),
	]

	employee = models.ForeignKey(Employee)
	date_time = models.DateTimeField(default=datetime.now)
	log_type = models.IntegerField(default='NA', choices=log_type_choices)
	is_used = models.BooleanField(default=False)

	@property
	def get_log_type(self):
		return get_choices_value(self.log_type_choices, self.log_type)


class Attendance(models.Model):


	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	date = models.DateField()
	remarks	= models.CharField(max_length=100, null=True, blank=True)

	class Meta:
		verbose_name_plural = 'Attendance'
	
	@property
	def total_minutes_late_in(self):
		ret = 0
		for alog in self.attendancelog_set.all():
			ret = ret + alog.minutes_late_in
		return ret
	total_minutes_late_in.fget.short_description = u'late in'	

	@property
	def total_minutes_early_out(self):
		ret = 0
		for alog in self.attendancelog_set.all():
			ret = ret + alog.minutes_early_out
		return ret
	total_minutes_early_out.fget.short_description = u'early out'

	@property
	def total_minutes_night_premium(self):
		ret = 0
		for alog in self.attendancelog_set.all():
			ret = ret + alog.minutes_night_premium
		return ret
	total_minutes_night_premium.fget.short_description = u'night'

	@property
	def total_minutes_ot_premium(self):
		ret = 0
		for alog in self.attendancelog_set.all():
			ret = ret + alog.minutes_ot_premium
		return ret
	total_minutes_ot_premium.fget.short_description = u'ot'


class AttendanceLog(models.Model):
	attendance = models.ForeignKey(Attendance)
	schedule_timetable = models.OneToOneField(ScheduleTimetable)
	final_date_time_in = models.DateTimeField(null=True, blank=True)
	final_date_time_out = models.DateTimeField(null=True, blank=True)
	minutes_late_in_actual = models.IntegerField(default=0)
	minutes_late_in = models.IntegerField(default=0)
	minutes_early_out = models.IntegerField(default=0)
	minutes_night_premium = models.IntegerField(default=0)
	minutes_ot_premium = models.IntegerField(default=0)
	is_absent = models.BooleanField(default=False)
	hours_deducted = models.IntegerField(default=0)
	hours_paid = models.IntegerField(default=0)
	application = models.ForeignKey(Application, null=True, blank=True)