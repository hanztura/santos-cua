from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.forms import model_to_dict

# pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Employee, Salary
from contacts.models import Contact

# forms
from .forms import EmployeeForm, SalaryForm


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
            form = EmployeeForm(initial={
                'contact':  contact,
                'abbr': contact.alias[:3],
            })
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
            new_employee = form.save()
            contact = Contact.objects.get(pk=new_employee.contact_id)
            contact.is_employee = True
            contact.save()
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


class Salaries():
    """

    """

    def index(request):
        q = request.GET.get('q')
        page = request.GET.get('page')

        # if search query is BLANK or NULL
        if not q:
            q = ''
            salary_list = Salary.objects.filter(employee__abbr__contains=q)
        else:
            salary_list = Salary.objects.filter(employee__abbr__contains=q)[:10]

        paginator = Paginator(salary_list, 10)

        try:
            salaries = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            salaries = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            salaries = paginator.page(paginator.num_pages)

        context = {
            'model_list': salaries,
            'page': page,
            'q': q,
            'index_url': 'employees:salary_index',
            'search_placeholder': 'type employee abbr'
        }

        return render(request, 'employees/salaries/index.html', context)

    def detail(request, id):
        salary = get_object_or_404(Salary, pk=id)

        form = SalaryForm(
            instance=salary,
            initial=model_to_dict(salary),
        )


        context = {
            'form' : form,
            'record': salary,
            'str_record_id': str(salary.id),
        }

        return render(
            request,
            'employees/salaries/detail.html',
            context
        )

    def update(request, id):
        if request.method == 'POST':
            salary = get_object_or_404(Salary, pk=id)
            form = SalaryForm(request.POST, instance=salary)
            
            context = {
                'form' : form,
                'record': salary,
            }

            fail = render(request, 'employees/salaries/detail.html', context)

            if form.has_changed():
                if form.is_valid():
                    form.save()
                else:    
                    return fail

            if request.POST.get('save'):
                return HttpResponseRedirect(reverse('employees:salary_index'))
            else:
                # save and continue
                return HttpResponseRedirect(reverse('employees:salary_detail', args=(salary.id,)))


    def destroy(request, id):
        salary = Salary.objects.get(id=id)
        # salary.is_deleted = True

        salary.delete()
        return HttpResponseRedirect(reverse('employees:salary_index'))