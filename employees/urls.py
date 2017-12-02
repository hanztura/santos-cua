from django.conf.urls import url

from . import views

app_name = 'employees'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<id>[0-9]+)/update/', views.update, name='update'),
    url(r'^new/(?P<id>[0-9]+)*$', views.new, name='new'),
    url(r'^create/', views.create, name='create'),
    url(r'^(?P<id>[0-9]+)/delete/$', views.destroy, name='destroy'),

    url(r'^payrollone/hr/salaries$', views.Salaries.index, name='salary_index'),
    url(r'^payrollone/hr/salaries/(?P<id>[0-9]+)/$', views.Salaries.detail, name='salary_detail'),
    url(r'^payrollone/hr/salaries/(?P<id>[0-9]+)/update/', views.Salaries.update, name='salary_update'),
    # url(r'^salaries/new/(?P<id>[0-9]+)*$', views.Salaries.new, name='salary_new'),
    # url(r'^salaries/create/', views.Salaries.create, name='salary_create'),
    url(r'^payrollone/hr/salaries/(?P<id>[0-9]+)/delete/$', views.Salaries.destroy, name='salary_destroy'),
]