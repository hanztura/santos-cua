from django.conf.urls import url

from . import views
from .models import Issuance, Application
from .forms import IssuanceForm, ApplicationForm


class IssuanceVars():
    context_search_placeholder = 'type employee abbr/lastname'
    model = Issuance
    model_name = 'issuance'
    model_name_plural = 'issuances'
    model_app = 'leaves'
    model_order_by = ('employee', 'leave', 'valid_on_year')

    model_url_index = model_app + ':' + model_name + '_index'
    model_url_detail = model_app + ':' + model_name + '_detail'
    model_url_new = model_app + ':' + model_name + '_new'
    model_url_create = model_app + ':' + model_name + '_create'
    model_url_update = model_app + ':' + model_name + '_update'
    model_url_destroy = model_app + ':' + model_name + '_destroy'

    model_template_index = model_app + '/' + model_name_plural + '/index.html'
    model_template_new = model_app + '/' + model_name_plural + '/new.html'
    model_template_detail = model_app + '/' + model_name_plural + '/detail.html'

    model_form = IssuanceForm


class ApplicationVars():
    context_search_placeholder = 'type employee abbr/lastname'
    model = Application
    model_name = 'application'
    model_name_plural = 'applications'
    model_app = 'leaves'
    model_order_by = ('date', 'employee', 'leave')

    model_url_index = model_app + ':' + model_name + '_index'
    model_url_detail = model_app + ':' + model_name + '_detail'
    model_url_new = model_app + ':' + model_name + '_new'
    model_url_create = model_app + ':' + model_name + '_create'
    model_url_update = model_app + ':' + model_name + '_update'
    model_url_destroy = model_app + ':' + model_name + '_destroy'

    model_template_index = model_app + '/' + model_name_plural + '/index.html'
    model_template_new = model_app + '/' + model_name_plural + '/new.html'
    model_template_detail = model_app + '/' + model_name_plural + '/detail.html'

    model_form = ApplicationForm

        
app_name = 'leaves'
urlpatterns = [
    url(r'^$', views.LeaveView.index, name='index'),

    url(r'^issuance$', views.IssuanceView.index, {'model_vars': IssuanceVars}, name='issuance_index'),
    url(r'^issuance/(?P<id>[0-9]+)/$', views.IssuanceView.detail, {'model_vars': IssuanceVars}, name='issuance_detail'),
    url(r'^issuance/(?P<id>[0-9]+)/update/', views.IssuanceView.update, {'model_vars': IssuanceVars}, name='issuance_update'),
    url(r'^issuance/new/(?P<id>[0-9]+)*$', views.IssuanceView.new, {'model_vars': IssuanceVars}, name='issuance_new'),
    url(r'^issuance/create/', views.IssuanceView.create, {'model_vars': IssuanceVars}, name='issuance_create'),
    url(r'^issuance/(?P<id>[0-9]+)/delete/$', views.IssuanceView.destroy, {'model_vars': IssuanceVars}, name='issuance_destroy'),

    url(r'^application$', views.ApplicationView.index, {'model_vars': ApplicationVars}, name='application_index'),
    url(r'^application/(?P<id>[0-9]+)/$', views.ApplicationView.detail, {'model_vars': ApplicationVars}, name='application_detail'),
    url(r'^application/(?P<id>[0-9]+)/update/', views.ApplicationView.update, {'model_vars': ApplicationVars}, name='application_update'),
    url(r'^application/new/(?P<id>[0-9]+)*$', views.ApplicationView.new, {'model_vars': ApplicationVars}, name='application_new'),
    url(r'^application/create/', views.ApplicationView.create, {'model_vars': ApplicationVars}, name='application_create'),
    url(r'^application/(?P<id>[0-9]+)/delete/$', views.ApplicationView.destroy, {'model_vars': ApplicationVars}, name='application_destroy'),
]