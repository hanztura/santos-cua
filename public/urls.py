from django.conf.urls import url

# file:///home/hanz/Tools/django-docs-1.11-en%20(1)/topics/auth/default.html#using-the-views
from django.contrib.auth import views as auth_views

from . import views

app_name = 'public'
urlpatterns = [
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^login/', auth_views.LoginView.as_view(template_name='public/login.html'), name='login'),
    url(r'^logmeout/$', views._logout, name='logout'),
    url(r'^$', views.HomeView.as_view(), name='home'),
]