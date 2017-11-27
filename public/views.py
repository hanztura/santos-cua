from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.views.generic import TemplateView

# Create your views here.
class HomeView(TemplateView):
    template_name = 'public/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class AboutView(TemplateView):
    template_name = 'public/about.html'


def home(request):
	return HttpResponseRedirect(reverse('public:home'))

def _login(request):
	if request.method == "GET":
		return render(request, 'public/login.html')

	if request.method == "POST":
		# user request to login to the system
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse('public:home'))
		else:
			return render(request, 'public/login.html')

def _logout(request):
		logout(request)
		
		return render(request, 'public/home.html', { 'logout': True })
