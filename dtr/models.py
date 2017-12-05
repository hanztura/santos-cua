from datetime import datetime
from django.db import models
from django import forms
from django.utils import timezone

from employees.models import Employee
from costcenters.models import Project, Work
from public.utils import get_choices_value

# Create your models here.
class Timetable(models.Model):
	time_in = models.TimeField('In')
	time_out = models.TimeField('Out')
	hours_npb = models.DecimalField('Non-paid Break', max_digits=4, decimal_places=2)
	hours_scheduled = models.DecimalField('Scheduled', max_digits=4, decimal_places=2)
	hours_paid = models.DecimalField('Paid', max_digits=4, decimal_places=2)
	remarks = models.CharField(max_length=100, null=True, blank=True)
	is_ot = models.BooleanField(default=False, verbose_name='OT')

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
	minutes_late_in = models.IntegerField(default=0)
	minutes_early_out = models.IntegerField(default=0)
	minutes_night_premium = models.IntegerField(default=0)
	minutes_ot_premium = models.IntegerField(default=0)
	is_absent = models.BooleanField(default=False)