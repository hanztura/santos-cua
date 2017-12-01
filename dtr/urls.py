from django.conf.urls import url

from . import views
from .models import Timetable
from .forms import TimetableForm

class TimetableVars():
    context_search_placeholder = 'type remarks'
    model = Timetable
    model_name = 'timetable'
    model_app = 'dtr'

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
        
app_name = 'dtr'
urlpatterns = [
    url(r'^$', views.DTRViews.index, name='index'),

    url(r'^timetables$', views.TimetableViews.index, {'model_vars': TimetableVars}, name='timetable_index'),
    url(r'^timetables/(?P<id>[0-9]+)/$', views.TimetableViews.detail, {'model_vars': TimetableVars}, name='timetable_detail'),
    url(r'^timetables/(?P<id>[0-9]+)/update/', views.TimetableViews.update, {'model_vars': TimetableVars}, name='timetable_update'),
    url(r'^timetables/new/(?P<id>[0-9]+)*$', views.TimetableViews.new, {'model_vars': TimetableVars}, name='timetable_new'),
    url(r'^timetables/create/', views.TimetableViews.create, {'model_vars': TimetableVars}, name='timetable_create'),
    url(r'^timetables/(?P<id>[0-9]+)/delete/$', views.TimetableViews.destroy, {'model_vars': TimetableVars}, name='timetable_destroy'),

    # url(r'^projects$', views.ProjectViews.index, name='project_index'),
    # url(r'^projects/(?P<id>[0-9]+)/$', views.ProjectViews.detail, name='project_detail'),
    # url(r'^projects/(?P<id>[0-9]+)/update/', views.ProjectViews.update, name='project_update'),
    # url(r'^projects/new/(?P<id>[0-9]+)*$', views.ProjectViews.new, name='project_new'),
    # url(r'^projects/create/', views.ProjectViews.create, name='project_create'),
    # url(r'^projects/(?P<id>[0-9]+)/delete/$', views.ProjectViews.destroy, name='project_destroy'),

    # url(r'^works$', views.WorkViews.index, name='work_index'),
    # url(r'^works/(?P<id>[0-9]+)/$', views.WorkViews.detail, name='work_detail'),
    # url(r'^works/(?P<id>[0-9]+)/update/', views.WorkViews.update, name='work_update'),
    # url(r'^works/new/(?P<id>[0-9]+)*$', views.WorkViews.new, name='work_new'),
    # url(r'^works/create/', views.WorkViews.create, name='work_create'),
    # url(r'^works/(?P<id>[0-9]+)/delete/$', views.WorkViews.destroy, name='work_destroy'),
]