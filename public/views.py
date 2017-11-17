from django.shortcuts import render

from django.views.generic import TemplateView

# Create your views here.
class HomeView(TemplateView):
    template_name = 'public/home.html'
    


class AboutView(TemplateView):
    template_name = 'public/about.html'