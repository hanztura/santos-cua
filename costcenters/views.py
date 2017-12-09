from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.forms import model_to_dict

# messages
# https://docs.djangoproject.com/en/dev/ref/contrib/messages/
from django.contrib import messages

# pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Branch, Project, Work
from .forms import BranchForm, ProjectForm, WorkForm
# Create your views here.


class CostCenterViews():
    """"""
    def index(request):
        return render(request, 'costcenters/index.html')


class BranchViews():
    def index(request):
        q = request.GET.get('q')
        page = request.GET.get('page')

        # if search query is BLANK or NULL
        if not q:
            q = ''
            branch_list = Branch.objects.filter(alias__contains=q)
        else:
            branch_list = Branch.objects.filter(alias__contains=q)[:10]

        paginator = Paginator(branch_list, 10)

        try:
            branches = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            branches = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            branches = paginator.page(paginator.num_pages)

        context = {
            'model_list': branches,
            'page': page,
            'q': q,
            'index_url': 'costcenters:branch_index',
            'search_placeholder': 'type branch alias',
        }

        return render(request, 'costcenters/branches/index.html', context)

    def detail(request, id):
        branch = get_object_or_404(Branch, pk=id)

        form = BranchForm(
            instance=branch,
            initial=model_to_dict(branch),
        )


        context = {
            'form' : form,
            'record': branch,
            'str_record_id': str(branch.id),
        }

        return render(
            request,
            'costcenters/branches/detail.html',
            context
        )

    def new(request, id=0):
        if request.method == "GET":
            form = BranchForm()
                
            context = {
                'form' : form,
            }

            return render(request, 'costcenters/branches/new.html', context)
        else:
            return render(request, 'costcenters:branch_index')

    def create(request):
        if request.method == "POST":
            # validate form
            form = BranchForm(request.POST)
            
            context = {
                'form' : form,
            }

            fail = render(request, 'costcenters/branches/new.html', context)

            if form.is_valid():
                new_branch = form.save()

                messages.success(request, 'Branch ' + new_branch.alias + ' created.')
            else:
                return fail

            return HttpResponseRedirect(reverse('costcenters:branch_index'))

    def update(request, id):
        if request.method == 'POST':
            branch = get_object_or_404(Branch, pk=id)
            form = BranchForm(request.POST, instance=branch)
            
            context = {
                'form' : form,
                'record': branch,
            }

            fail = render(request, 'costcenters/branches/detail.html', context)

            if form.has_changed():
                if form.is_valid():
                    form.save()
                else:    
                    return fail

            if request.POST.get('save'):
                return HttpResponseRedirect(reverse('costcenters:branch_index'))
            else:
                # save and continue
                return HttpResponseRedirect(reverse('costcenters:branch_detail', args=(id,)))

    def destroy(request, id):
        branch = Branch.objects.get(id=id)
        branch.delete()

        return HttpResponseRedirect(reverse('costcenters:branch_index'))


class ProjectViews():
    def index(request):
        q = request.GET.get('q')
        page = request.GET.get('page')

        # if search query is BLANK or NULL
        if not q:
            q = ''
            project_list = Project.objects.filter(alias__contains=q)
        else:
            project_list = Project.objects.filter(alias__contains=q)[:10]

        paginator = Paginator(project_list, 10)

        try:
            branches = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            branches = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            branches = paginator.page(paginator.num_pages)

        context = {
            'model_list': branches,
            'page': page,
            'q': q,
            'index_url': 'costcenters:project_index',
            'search_placeholder': 'type project alias',
        }

        return render(request, 'costcenters/projects/index.html', context)

    def new(request, id=0):
        if request.method == "GET":
            form = ProjectForm()
                
            context = {
                'form' : form,
            }

            return render(request, 'costcenters/projects/new.html', context)
        else:
            return HttpResponseRedirect(reverse('costcenters:project_index'))

    def detail(request, id):
        project = get_object_or_404(Project, pk=id)

        form = ProjectForm(
            instance=project,
            initial=model_to_dict(project),
        )


        context = {
            'form' : form,
            'record': project,
            'str_record_id': str(project.id),
        }

        return render(
            request,
            'costcenters/projects/detail.html',
            context
        )

    def create(request):
        if request.method == "POST":
            # validate form
            form = ProjectForm(request.POST)
            
            context = {
                'form' : form,
            }

            fail = render(request, 'costcenters/projects/new.html', context)

            if form.is_valid():
                new_project = form.save()
            else:
                return fail

            return HttpResponseRedirect(reverse('costcenters:project_index'))

    def update(request, id):
        if request.method == 'POST':
            project = get_object_or_404(Project, pk=id)
            form = ProjectForm(request.POST, instance=project)
            
            context = {
                'form' : form,
                'record': project,
            }

            fail = render(request, 'costcenters/projects/detail.html', context)

            if form.has_changed():
                if form.is_valid():
                    form.save()
                else:    
                    return fail

            if request.POST.get('save'):
                return HttpResponseRedirect(reverse('costcenters:project_index'))
            else:
                # save and continue
                return HttpResponseRedirect(reverse('costcenters:project_detail', args=(id,)))

    def destroy(request, id):
        project = Project.objects.get(id=id)
        project.delete()

        return HttpResponseRedirect(reverse('costcenters:project_index'))


class WorkViews():
    def index(request):
        q = request.GET.get('q')
        page = request.GET.get('page')

        # if search query is BLANK or NULL
        if not q:
            q = ''
            work_list = Work.objects.filter(work_name__contains=q)
        else:
            work_list = Work.objects.filter(work_name__contains=q)[:10]

        paginator = Paginator(work_list, 10)

        try:
            works = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            works = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            works = paginator.page(paginator.num_pages)

        context = {
            'model_list': works,
            'page': page,
            'q': q,
            'index_url': 'costcenters:work_index',
            'search_placeholder': 'type work name',
        }

        return render(request, 'costcenters/works/index.html', context)

    def new(request, id=0):
        if request.method == "GET":
            form = WorkForm()
                
            context = {
                'form' : form,
            }

            return render(request, 'costcenters/works/new.html', context)
        else:
            return HttpResponseRedirect(reverse('costcenters:work_index'))

    def detail(request, id):
        work = get_object_or_404(Work, pk=id)

        form = WorkForm(
            instance=work,
            initial=model_to_dict(work),
        )


        context = {
            'form' : form,
            'record': work,
            'str_record_id': str(work.id),
        }

        return render(
            request,
            'costcenters/works/detail.html',
            context
        )

    def create(request):
        if request.method == "POST":
            # validate form
            form = WorkForm(request.POST)
            
            context = {
                'form' : form,
            }

            fail = render(request, 'costcenters/works/new.html', context)

            if form.is_valid():
                new_work = form.save()
            else:
                return fail

            return HttpResponseRedirect(reverse('costcenters:work_index'))

    def update(request, id):
        if request.method == 'POST':
            work = get_object_or_404(Work, pk=id)
            form = WorkForm(request.POST, instance=work)
            
            context = {
                'form' : form,
                'record': work,
            }

            fail = render(request, 'costcenters/works/detail.html', context)

            if form.has_changed():
                if form.is_valid():
                    form.save()
                else:    
                    return fail

            if request.POST.get('save'):
                return HttpResponseRedirect(reverse('costcenters:work_index'))
            else:
                # save and continue
                return HttpResponseRedirect(reverse('costcenters:work_detail', args=(id,)))

    def destroy(request, id):
        work = Project.objects.get(id=id)
        work.delete()

        return HttpResponseRedirect(reverse('costcenters:work_index'))


class HolidayView():

    def index(request, model_vars):
        q = request.GET.get('q')
        page = request.GET.get('page')

        # if search query is BLANK or NULL
        # if not q:
        record_list = model_vars.model.objects.all().order_by( model_vars.model_order_by )
        # else:
        #     record_list = model_vars.model.objects.filter(Q(city__city__contains=q) | Q(city__alias__contains=q)).order_by( *model_vars.model_order_by )[:10]

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
                messages.success(request, 'successfully created ' + model_vars.model_name+ ' to #ofcities' + str(new_record.cities.count()) + ' on ' + str(new_record.date) + '.')
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

            messages.success(request, 'successfully UPDATED ' + model_vars.model_name + ' of ' + record.cities.count())
            
            if request.POST.get('save'):
                return HttpResponseRedirect(reverse(model_vars.model_url_index))
            else:
                # save and continue
                return HttpResponseRedirect(reverse(model_vars.model_url_detail, args=(id,)))

    def destroy(request, model_vars, id):
        record = model_vars.model.objects.get(id=id)
        deleted_alias = record.cities.count()
        deleted_date = record.date
        record.delete()
        messages.warning(request, 'successfully DELETED ' + model_vars.model_name+ ' of ' + str(deleted_alias) + ' on ' + str(deleted_date) + '.')
        return HttpResponseRedirect(reverse(model_vars.model_url_index))  