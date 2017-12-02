from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

# from .forms import IssuanceForm, ApplicationForm
# from .models import Issuance, Application

class LeaveView():
    def index(request):
        return render(request, 'leaves/index.html')


class IssuanceView():

    def index(request, model_vars):
        q = request.GET.get('q')
        page = request.GET.get('page')

        # if search query is BLANK or NULL
        if not q:
            record_list = model_vars.model.objects.all().order_by( *model_vars.model_order_by )
        else:
            record_list = model_vars.model.objects.filter(Q(employee__abbr__contains=q) | Q(employee__contact__last_name__contains=q)).order_by( *model_vars.model_order_by )[:10]

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
                messages.success(request, 'successfully created ' + model_vars.model_name + ' of ' + str(new_record.get_leave) + ' for ' + str(new_record.employee) + '.')
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
                    messages.success(request, 'successfully UPDATED ' + model_vars.model_name + ' of ' + str(new_record.get_leave) + ' for ' + str(new_record.employee) + '.')
                else:    
                    return fail
            
            if request.POST.get('save'):
                return HttpResponseRedirect(reverse(model_vars.model_url_index))
            else:
                # save and continue
                return HttpResponseRedirect(reverse(model_vars.model_url_detail, args=(id,)))

    def destroy(request, model_vars, id):
        record = model_vars.model.objects.get(id=id)
        deleted_alias = record.employee
        deleted_leave = record.get_leave
        record.delete()
        messages.warning(request, 'successfully DELETED ' + model_vars.model_name+ ' of ' + str(deleted_leave) + ' for ' + str(deleted_alias) + '.')
        return HttpResponseRedirect(reverse(model_vars.model_url_index))


class ApplicationView():

    def index(request, model_vars):
        q = request.GET.get('q')
        page = request.GET.get('page')

        # if search query is BLANK or NULL
        if not q:
            record_list = model_vars.model.objects.all().order_by( *model_vars.model_order_by )
        else:
            record_list = model_vars.model.objects.filter(Q(employee__abbr__contains=q) | Q(employee__contact__last_name__contains=q)).order_by( *model_vars.model_order_by )[:10]

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
                messages.success(request, 'successfully created ' + model_vars.model_name + ' of ' + str(new_record.get_leave) + ' for ' + str(new_record.employee) + '.')
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
                    messages.success(request, 'successfully UPDATED ' + model_vars.model_name + ' of ' + str(new_record.get_leave) + ' for ' + str(new_record.employee) + '.')
                else:    
                    return fail
            
            if request.POST.get('save'):
                return HttpResponseRedirect(reverse(model_vars.model_url_index))
            else:
                # save and continue
                return HttpResponseRedirect(reverse(model_vars.model_url_detail, args=(id,)))

    def destroy(request, model_vars, id):
        record = model_vars.model.objects.get(id=id)
        deleted_alias = record.employee
        deleted_leave = record.get_leave
        record.delete()
        messages.warning(request, 'successfully DELETED ' + model_vars.model_name+ ' of ' + str(deleted_leave) + ' for ' + str(deleted_alias) + '.')
        return HttpResponseRedirect(reverse(model_vars.model_url_index))   