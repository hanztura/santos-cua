from django.conf.urls import url

from .views import ClientViews, BirViews, DeadlineViews, ComplianceViews

app_name = 'compliance'
urlpatterns = [
    # compliance home
    url(r'^$', ComplianceViews.index, name='index'),

    # clients
    url(r'^clients$', ClientViews.index, name='client_index'),
    url(r'^clients/(?P<id>[0-9]+)/$', ClientViews.detail, name='client_detail'),
    url(r'^clients/(?P<id>[0-9]+)/update/', ClientViews.update, name='client_update'),
    url(r'^clients/new/(?P<id>[0-9]+)*$', ClientViews.new, name='client_new'),
    url(r'^clients/create/', ClientViews.create, name='client_create'),
    url(r'^clients/(?P<id>[0-9]+)/delete/$', ClientViews.destroy, name='client_destroy'),
    url(r'^clients/(?P<id>[0-9]+)/deactivate/$', ClientViews.deactivate, name='client_deactivate'),
    url(r'^clients/(?P<id>[0-9]+)/activate/$', ClientViews.activate, name='client_activate'),
    # bir
    url(r'^bir$', BirViews.index, name='bir_index'),
    url(r'^bir/(?P<id>[0-9]+)/$', BirViews.detail, name='bir_detail'),
    url(r'^bir/(?P<id>[0-9]+)/update/', BirViews.update, name='bir_update'),
    url(r'^bir/new$', BirViews.new, name='bir_new'),
    url(r'^bir/create/', BirViews.create, name='bir_create'),
    url(r'^bir/(?P<id>[0-9]+)/delete/$', BirViews.destroy, name='bir_destroy'),
    
    #  deadlines
    url(r'^deadlines$', DeadlineViews.index, name='deadline_index'),
    url(r'^deadlines/(?P<id>[0-9]+)/$', DeadlineViews.detail, name='deadline_detail'),
    url(r'^deadlines/(?P<id>[0-9]+)/update/', DeadlineViews.update, name='deadline_update'),
    url(r'^deadlines/new$', DeadlineViews.new, name='deadline_new'),
    url(r'^deadlines/create/', DeadlineViews.create, name='deadline_create'),
    url(r'^deadlines/(?P<id>[0-9]+)/delete/$', DeadlineViews.destroy, name='deadline_destroy'),
    
]