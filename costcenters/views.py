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