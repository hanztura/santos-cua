"""santosCua URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

# serving files in /media
from django.conf import settings
from django.conf.urls.static import static

# django-notifications
# https://github.com/django-notifications/django-notifications
import notifications.urls

from public.views import home

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')), # admin docs
    url(r'^admin/', admin.site.urls, name='admin'),
    
    url(r'^contacts/', include('contacts.urls')),

    url(r'^employees/', include('employees.urls')),

    url(r'^compliance/', include('compliance.urls')),


    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    
    url(r'^home/', home),
    url(r'^', include('public.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
