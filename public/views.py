from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # pagination
from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
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

class HolidayView():

    def index(request, model_vars):
        q = request.GET.get('q')
        page = request.GET.get('page')

        # if search query is BLANK or NULL
        if not q:
            record_list = model_vars.model.objects.all().order_by( *model_vars.model_order_by )
        else:
            record_list = model_vars.model.objects.filter(Q(city__city__contains=q) | Q(city__alias__contains=q)).order_by( *model_vars.model_order_by )[:10]

        paginator = Paginator(record_list, 10)

        try:
            records = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            records = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            records = paginator.page(paginator.num_pages)

        context = {
            'model_list': records,
            'page': page,
            'q': q,
            'index_url': model_vars.model_url_index,
            'search_placeholder': model_vars.context_search_placeholder,
            'model_name': model_vars.model_name,
            'model_name_plural': model_vars.model_name_plural,
            'model_url_new': model_vars.model_url_new,
            'model_url_detail': model_vars.model_url_detail,
            'model_url_update': model_vars.model_url_update,
            'model_url_destroy': model_vars.model_url_destroy,
        }

        return render(request, model_vars.model_template_index, context)

    def new(request, model_vars, id=0):
        if request.method == "GET":
            form = model_vars.model_form()

            context = {
                'form' : form,

                'model': model_vars.model,
                'model_name': model_vars.model_name,
                'model_app': model_vars.model_app,
                'model_url_index': model_vars.model_url_index,
                'model_url_new': model_vars.model_url_new,
                'model_url_create': model_vars.model_url_create,
            }

            return render(request, model_vars.model_template_new, context)
        else:
            return HttpResponseRedirect(reverse(model_vars.model_url_index))

    def detail(request, model_vars, id):
        record = get_object_or_404(model_vars.model, pk=id)

        form = model_vars.model_form(
            instance=record,
            initial=model_to_dict(record),
        )
        


        context = {
            'form' : form,
            'record': record,
            'str_record_id': str(record.id),

            'model': model_vars.model,
            'model_name': model_vars.model_name,
            'model_name_plural': model_vars.model_name_plural,
            'model_app': model_vars.model_app,
            'model_url_index': model_vars.model_url_index,
            'model_url_update': model_vars.model_url_update,
            'model_url_destroy': model_vars.model_url_destroy,
        }

        return render(
            request,
            model_vars.model_template_detail,
            context
        )

    def create(request, model_vars):
        if request.method == "POST":
            # validate form
            form = model_vars.model_form(request.POST)
            
            context = {
                'form' : form,

                'model': model_vars.model,
                'model_name': model_vars.model_name,
                'model_app': model_vars.model_app,
                'model_url_index': model_vars.model_url_index,
                'model_url_new': model_vars.model_url_new,
                'model_url_create': model_vars.model_url_create,
            }

            fail = render(request, model_vars.model_template_new, context)

            if form.is_valid():
                new_record = form.save()
                messages.success(request, 'successfully created ' + model_vars.model_name+ ' of ' + str(new_record.city.alias) + ' on ' + str(new_record.date) + '.')
            else:
                return fail

            return HttpResponseRedirect(reverse(model_vars.model_url_index))

    def update(request, model_vars, id):
        if request.method == 'POST':
            record = get_object_or_404(model_vars.model, pk=id)
            form = model_vars.model_form(request.POST, instance=record)
            
            context = {
                'form' : form,
                'record': record,

                'model': model_vars.model,
                'model_name': model_vars.model_name,
                'model_app': model_vars.model_app,
                'model_url_index': model_vars.model_url_index,
                'model_url_update': model_vars.model_url_update,
                'model_url_destroy': model_vars.model_url_destroy,
            }

            fail = render(request, model_vars.model_template_detail, context)

            if form.has_changed():
                if form.is_valid():
                    new_record = form.save()
                else:    
                    return fail

            messages.success(request, 'successfully UPDATED ' + model_vars.model_name + ' of ' + record.city.alias)
            
            if request.POST.get('save'):
                return HttpResponseRedirect(reverse(model_vars.model_url_index))
            else:
                # save and continue
                return HttpResponseRedirect(reverse(model_vars.model_url_detail, args=(id,)))

    def destroy(request, model_vars, id):
        record = model_vars.model.objects.get(id=id)
        deleted_alias = record.city.alias
        deleted_date = record.date
        record.delete()
        messages.warning(request, 'successfully DELETED ' + model_vars.model_name+ ' of ' + str(deleted_alias) + ' on ' + str(deleted_date) + '.')
        return HttpResponseRedirect(reverse(model_vars.model_url_index))   


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
