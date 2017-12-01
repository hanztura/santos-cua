from django.conf.urls import url

from . import views

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
]