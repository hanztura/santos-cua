from django.conf.urls import url

# file:///home/hanz/Tools/django-docs-1.11-en%20(1)/topics/auth/default.html#using-the-views
from django.contrib.auth import views as auth_views

from . import views
# from .models import Holiday
# from .forms import HolidayForm


# class HolidayVars():
#     context_search_placeholder = 'type city/alias'
#     model = Holiday
#     model_name = 'holiday'
#     model_name_plural = 'holidays'
#     model_app = 'public'
#     model_order_by = ('date', 'city')

#     model_url_index = model_app + ':' + model_name + '_index'
#     model_url_detail = model_app + ':' + model_name + '_detail'
#     model_url_new = model_app + ':' + model_name + '_new'
#     model_url_create = model_app + ':' + model_name + '_create'
#     model_url_update = model_app + ':' + model_name + '_update'
#     model_url_destroy = model_app + ':' + model_name + '_destroy'

#     model_template_index = model_app + '/' + model_name_plural + '/index.html'
#     model_template_new = model_app + '/' + model_name_plural + '/new.html'
#     model_template_detail = model_app + '/' + model_name_plural + '/detail.html'

#     model_form = HolidayForm


app_name = 'public'
urlpatterns = [
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^login/', auth_views.LoginView.as_view(template_name='public/login.html'), name='login'),
    url(r'^logmeout/$', views._logout, name='logout'),

    # url(r'^holidays$', views.HolidayView.index, {'model_vars': HolidayVars}, name='holiday_index'),
    # url(r'^holidays/(?P<id>[0-9]+)/$', views.HolidayView.detail, {'model_vars': HolidayVars}, name='holiday_detail'),
    # url(r'^holidays/(?P<id>[0-9]+)/update/', views.HolidayView.update, {'model_vars': HolidayVars}, name='holiday_update'),
    # url(r'^holidays/new/(?P<id>[0-9]+)*$', views.HolidayView.new, {'model_vars': HolidayVars}, name='holiday_new'),
    # url(r'^holidays/create/', views.HolidayView.create, {'model_vars': HolidayVars}, name='holiday_create'),
    # url(r'^holidays/(?P<id>[0-9]+)/delete/$', views.HolidayView.destroy, {'model_vars': HolidayVars}, name='holiday_destroy'),

    url(r'^$', views.HomeView.as_view(), name='home'),
]