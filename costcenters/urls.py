from django.conf.urls import url

from . import views
from .models import Holiday
from .forms import HolidayForm


class HolidayVars():


    context_search_placeholder = 'soon'
    model = Holiday
    model_name = 'holiday'
    model_name_plural = 'holidays'
    model_app = 'costcenters'
    model_order_by = ('date')

    model_url_index = model_app + ':' + model_name + '_index'
    model_url_detail = model_app + ':' + model_name + '_detail'
    model_url_new = model_app + ':' + model_name + '_new'
    model_url_create = model_app + ':' + model_name + '_create'
    model_url_update = model_app + ':' + model_name + '_update'
    model_url_destroy = model_app + ':' + model_name + '_destroy'

    model_template_index = model_app + '/' + model_name_plural + '/index.html'
    model_template_new = model_app + '/' + model_name_plural + '/new.html'
    model_template_detail = model_app + '/' + model_name_plural + '/detail.html'

    model_form = HolidayForm

    
app_name = 'costcenters'
urlpatterns = [
    url(r'^$', views.CostCenterViews.index, name='index'),

    url(r'^branches$', views.BranchViews.index, name='branch_index'),
    url(r'^branches/(?P<id>[0-9]+)/$', views.BranchViews.detail, name='branch_detail'),
    url(r'^branches/(?P<id>[0-9]+)/update/', views.BranchViews.update, name='branch_update'),
    url(r'^branches/new/(?P<id>[0-9]+)*$', views.BranchViews.new, name='branch_new'),
    url(r'^branches/create/', views.BranchViews.create, name='branch_create'),
    url(r'^branches/(?P<id>[0-9]+)/delete/$', views.BranchViews.destroy, name='branch_destroy'),

    url(r'^projects$', views.ProjectViews.index, name='project_index'),
    url(r'^projects/(?P<id>[0-9]+)/$', views.ProjectViews.detail, name='project_detail'),
    url(r'^projects/(?P<id>[0-9]+)/update/', views.ProjectViews.update, name='project_update'),
    url(r'^projects/new/(?P<id>[0-9]+)*$', views.ProjectViews.new, name='project_new'),
    url(r'^projects/create/', views.ProjectViews.create, name='project_create'),
    url(r'^projects/(?P<id>[0-9]+)/delete/$', views.ProjectViews.destroy, name='project_destroy'),

    url(r'^works$', views.WorkViews.index, name='work_index'),
    url(r'^works/(?P<id>[0-9]+)/$', views.WorkViews.detail, name='work_detail'),
    url(r'^works/(?P<id>[0-9]+)/update/', views.WorkViews.update, name='work_update'),
    url(r'^works/new/(?P<id>[0-9]+)*$', views.WorkViews.new, name='work_new'),
    url(r'^works/create/', views.WorkViews.create, name='work_create'),
    url(r'^works/(?P<id>[0-9]+)/delete/$', views.WorkViews.destroy, name='work_destroy'),

    url(r'^holidays$', views.HolidayView.index, {'model_vars': HolidayVars}, name='holiday_index'),
    url(r'^holidays/(?P<id>[0-9]+)/$', views.HolidayView.detail, {'model_vars': HolidayVars}, name='holiday_detail'),
    url(r'^holidays/(?P<id>[0-9]+)/update/', views.HolidayView.update, {'model_vars': HolidayVars}, name='holiday_update'),
    url(r'^holidays/new/(?P<id>[0-9]+)*$', views.HolidayView.new, {'model_vars': HolidayVars}, name='holiday_new'),
    url(r'^holidays/create/', views.HolidayView.create, {'model_vars': HolidayVars}, name='holiday_create'),
    url(r'^holidays/(?P<id>[0-9]+)/delete/$', views.HolidayView.destroy, {'model_vars': HolidayVars}, name='holiday_destroy'),
]