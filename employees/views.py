from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.forms import model_to_dict

# pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Employee
from contacts.models import Contact

# forms
from .forms import EmployeeForm


def index(request):
    q = request.GET.get('q')
    page = request.GET.get('page')

    # if search query is BLANK or NULL
    if not q:
        q = ''
        employee_list = Employee.objects.filter(abbr__contains=q).order_by('abbr')
    else:
        employee_list = Employee.objects.filter(abbr__contains=q).order_by('abbr')[:10]

    paginator = Paginator(employee_list, 10)

    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        employees = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        employees = paginator.page(paginator.num_pages)

    context = {
        'employee_list': employees,
        'page': page,
        'q': q,
        'index_url': 'employees:index',
        'search_placeholder': 'type employee abbr'
    }

    return render(request, 'employees/index_cards.html', context)

def detail(request, id):
    employee = get_object_or_404(Employee, pk=id)

    form = EmployeeForm(
        instance=employee,
        initial=model_to_dict(employee),
    )


    context = {
        'form' : form,
        'employee': employee,
        'str_employee_id': str(employee.id),
    }

    return render(
        request,
        'employees/detail.html',
        context
    )

def new(request, id=0):
    if request.method == "GET":
        if ((not id == 0) and (not id == None)):
            contact = Contact.objects.get(pk=id)
            form = EmployeeForm(initial={'contact':  contact})
        else:
            form = EmployeeForm()
            
        context = {
            'form' : form,
        }

        return render(request, 'employees/new.html', context)
    else:
        return HttpResponseRedirect(reverse('employees:index'))

def create(request):
    if request.method == "POST":
        # validate form
        form = EmployeeForm(request.POST)
        
        context = {
            'form' : form,
        }

        fail = render(request, 'employees/new.html', context)

        if form.is_valid():
            new_contact = form.save()
        else:
            return fail

        return HttpResponseRedirect(reverse('employees:index'))

def update(request, id):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, pk=id)
        form = EmployeeForm(request.POST, instance=employee)
        
        context = {
            'form' : form,
            'employee': employee,
        }

        fail = render(request, 'employees/detail.html', context)

        if form.has_changed():
            if form.is_valid():
                form.save()
            else:    
                return fail

        return HttpResponseRedirect(reverse('employees:index'))

def destroy(request, id):
    employee = Employee.objects.get(id=id)
    employee.is_deleted = True

    employee.save()
    return HttpResponseRedirect(reverse('employees:index'))