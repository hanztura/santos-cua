from django.conf.urls import url

from . import views

app_name = 'public'
urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
]