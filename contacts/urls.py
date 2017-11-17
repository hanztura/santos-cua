from django.conf.urls import url

from . import views

app_name = 'contacts'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<contact_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<contact_id>[0-9]+)/update/', views.update, name='update'),
    url(r'^new/$', views.new, name='new'),
    url(r'^create/', views.create, name='create'),
    url(r'^(?P<contact_id>[0-9]+)/delete/$', views.destroy, name='destroy'),
]