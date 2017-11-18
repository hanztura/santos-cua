from django.conf.urls import url

from .views import ClientViews, BirViews, StatusViews, ComplianceViews

app_name = 'compliance'
urlpatterns = [
    # compliance home
    url(r'^$', ComplianceViews.index, name='index'),

    # clients
    url(r'^engagements$', ClientViews.index, name='client_index'),
    url(r'^engagements/(?P<id>[0-9]+)/$', ClientViews.detail, name='client_detail'),
    url(r'^engagements/(?P<id>[0-9]+)/update/', ClientViews.update, name='client_update'),
    url(r'^engagements/new/(?P<id>[0-9]+)*$', ClientViews.new, name='client_new'),
    url(r'^engagements/create/', ClientViews.create, name='client_create'),
    url(r'^engagements/(?P<id>[0-9]+)/delete/$', ClientViews.destroy, name='client_destroy'),
    url(r'^engagements/(?P<id>[0-9]+)/deactivate/$', ClientViews.deactivate, name='client_deactivate'),
    url(r'^engagements/(?P<id>[0-9]+)/activate/$', ClientViews.activate, name='client_activate'),
    
    # bir
    url(r'^bir$', BirViews.index, name='bir_index'),
    url(r'^bir/(?P<id>[0-9]+)/delete/$', BirViews.destroy, name='bir_destroy'),
    
    #  status
    url(r'^status$', StatusViews.index, name='status_index'),
    url(r'^status/(?P<id>[0-9]+)/$', StatusViews.detail, name='status_detail'),
    url(r'^status/(?P<id>[0-9]+)/update/', StatusViews.update, name='status_update'),
    url(r'^status/new$', StatusViews.new, name='status_new'),
    url(r'^status/create/', StatusViews.create, name='status_create'),
    url(r'^status/(?P<id>[0-9]+)/delete/$', StatusViews.destroy, name='status_destroy'),
    
]