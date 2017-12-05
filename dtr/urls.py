from django.conf.urls import url

from . import views
from .models import Timetable, Schedule, ScheduleTimetable, Log, Attendance, AttendanceLog
from .forms import TimetableForm, ScheduleForm, LogForm, AttendanceForm, AttendanceLogFormSet


class TimetableVars():
    context_search_placeholder = 'type remarks'
    model = Timetable
    model_name = 'timetable'
    model_app = 'dtr'
    model_order_by = ('time_in', 'time_out')

    model_url_index = 'dtr:timetable_index'
    model_url_detail = 'dtr:timetable_detail'
    model_url_new = 'dtr:timetable_new'
    model_url_create = 'dtr:timetable_create'
    model_url_update = 'dtr:timetable_update'
    model_url_destroy = 'dtr:timetable_destroy'

    model_template_index = 'dtr/timetables/index.html'
    model_template_new = 'dtr/timetables/new.html'
    model_template_detail = 'dtr/timetables/detail.html'

    model_form = TimetableForm


class ScheduleVars():
    context_search_placeholder = 'type employee abbr/lastname'
    model = Schedule
    model_name = 'schedule'
    model_name_plural = 'schedules'
    model_app = 'dtr'
    model_order_by = ('date', 'employee')

    model_url_index = 'dtr:' + model_name + '_index'
    model_url_detail = 'dtr:' + model_name + '_detail'
    model_url_new = 'dtr:' + model_name + '_new'
    model_url_create = 'dtr:' + model_name + '_create'
    model_url_update = 'dtr:' + model_name + '_update'
    model_url_destroy = 'dtr:' + model_name + '_destroy'

    model_template_index = 'dtr/' + model_name_plural + '/index.html'
    model_template_new = 'dtr/' + model_name_plural + '/new.html'
    model_template_detail = 'dtr/' + model_name_plural + '/detail.html'

    model_form = ScheduleForm


class LogVars():
    context_search_placeholder = 'type employee abbr/lastname'
    model = Log
    model_name = 'log'
    model_name_plural = 'logs'
    model_app = 'dtr'
    model_order_by = ('date_time', 'employee', 'id')

    model_url_index = 'dtr:' + model_name + '_index'
    model_url_detail = 'dtr:' + model_name + '_detail'
    model_url_new = 'dtr:' + model_name + '_new'
    model_url_create = 'dtr:' + model_name + '_create'
    model_url_update = 'dtr:' + model_name + '_update'
    model_url_destroy = 'dtr:' + model_name + '_destroy'

    model_template_index = 'dtr/' + model_name_plural + '/index.html'
    model_template_new = 'dtr/' + model_name_plural + '/new.html'
    model_template_detail = 'dtr/' + model_name_plural + '/detail.html'

    model_form = LogForm


class AttendanceVars():
    context_search_placeholder = 'type employee abbr/lastname'
    model = Attendance
    model_name = 'attendance'
    model_name_plural = 'attendance'
    model_app = 'dtr'
    model_order_by = ('date', 'employee')

    model_url_index = 'dtr:' + model_name + '_index'
    model_url_detail = 'dtr:' + model_name + '_detail'
    model_url_new = 'dtr:' + model_name + '_new'
    model_url_create = 'dtr:' + model_name + '_create'
    model_url_update = 'dtr:' + model_name + '_update'
    model_url_destroy = 'dtr:' + model_name + '_destroy'

    model_template_index = 'dtr/' + model_name_plural + '/index.html'
    model_template_new = 'dtr/' + model_name_plural + '/new.html'
    model_template_detail = 'dtr/' + model_name_plural + '/detail.html'

    model_form = AttendanceForm

        
app_name = 'dtr'
urlpatterns = [
    url(r'^$', views.DTRViews.index, name='index'),

    url(r'^timetables$', views.TimetableViews.index, {'model_vars': TimetableVars}, name='timetable_index'),
    url(r'^timetables/(?P<id>[0-9]+)/$', views.TimetableViews.detail, {'model_vars': TimetableVars}, name='timetable_detail'),
    url(r'^timetables/(?P<id>[0-9]+)/update/', views.TimetableViews.update, {'model_vars': TimetableVars}, name='timetable_update'),
    url(r'^timetables/new/(?P<id>[0-9]+)*$', views.TimetableViews.new, {'model_vars': TimetableVars}, name='timetable_new'),
    url(r'^timetables/create/', views.TimetableViews.create, {'model_vars': TimetableVars}, name='timetable_create'),
    url(r'^timetables/(?P<id>[0-9]+)/delete/$', views.TimetableViews.destroy, {'model_vars': TimetableVars}, name='timetable_destroy'),

    url(r'^schedules$', views.ScheduleViews.index, {'model_vars': ScheduleVars}, name='schedule_index'),
    url(r'^schedules/(?P<id>[0-9]+)/$', views.ScheduleViews.detail, {'model_vars': ScheduleVars}, name='schedule_detail'),
    url(r'^schedules/(?P<id>[0-9]+)/update/', views.ScheduleViews.update, {'model_vars': ScheduleVars}, name='schedule_update'),
    url(r'^schedules/new/(?P<id>[0-9]+)*$', views.ScheduleViews.new, {'model_vars': ScheduleVars}, name='schedule_new'),
    url(r'^schedules/create/', views.ScheduleViews.create, {'model_vars': ScheduleVars}, name='schedule_create'),
    url(r'^schedules/(?P<id>[0-9]+)/delete/$', views.ScheduleViews.destroy, {'model_vars': ScheduleVars}, name='schedule_destroy'),

    url(r'^logs$', views.LogViews.index, {'model_vars': LogVars}, name='log_index'),
    url(r'^logs/(?P<id>[0-9]+)/$', views.LogViews.detail, {'model_vars': LogVars}, name='log_detail'),
    url(r'^logs/(?P<id>[0-9]+)/update/', views.LogViews.update, {'model_vars': LogVars}, name='log_update'),
    url(r'^logs/new/(?P<id>[0-9]+)*$', views.LogViews.new, {'model_vars': LogVars}, name='log_new'),
    url(r'^logs/create/', views.LogViews.create, {'model_vars': LogVars}, name='log_create'),
    url(r'^logs/(?P<id>[0-9]+)/delete/$', views.LogViews.destroy, {'model_vars': LogVars}, name='log_destroy'),

    url(r'^attendance$', views.AttendanceViews.index, {'model_vars': AttendanceVars}, name='attendance_index'),
    url(r'^attendance/(?P<id>[0-9]+)/$', views.AttendanceViews.detail, {'model_vars': AttendanceVars}, name='attendance_detail'),
    url(r'^attendance/(?P<id>[0-9]+)/update/', views.AttendanceViews.update, {'model_vars': AttendanceVars}, name='attendance_update'),
    url(r'^attendance/new/(?P<id>[0-9]+)*$', views.AttendanceViews.new, {'model_vars': AttendanceVars}, name='attendance_new'),
    url(r'^attendance/create/', views.AttendanceViews.create, {'model_vars': AttendanceVars}, name='attendance_create'),
    url(r'^attendance/(?P<id>[0-9]+)/delete/$', views.AttendanceViews.destroy, {'model_vars': AttendanceVars}, name='attendance_destroy'),
]