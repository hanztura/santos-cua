from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.forms import model_to_dict

# pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Client, ClientPractitioner, BirCompliance, BirDeadline, DeadlineStatus
from employees.models import Employee

# forms
from .forms import ClientForm

class ComplianceViews():
    """View functions of Compliance main-app"""
    def index(request):
        return render(request, 'compliance/index.html')

class ClientViews():
    """View functions of Client sub-app"""
    def index(request):
        client_list = Client.objects.filter(is_deleted=False)
        paginator = Paginator(client_list, 25)

        page = request.GET.get('page')
        try:
            client = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            client = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            client = paginator.page(paginator.num_pages)

        context = {
            'client_list': client,
        }

        return render(request, 'compliance/clients/index.html', context)

    def detail(request, id):
        model = get_object_or_404(Client, pk=id)

        form = ClientForm(
            instance=model,
            initial=model_to_dict(model),
        )


        context = {
            'form' : form,
            'model': model,
            'str_model_id': str(model.id),
        }

        return render(
            request,
            'compliance/clients/detail.html',
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
        if (request.method == "POST"):
            client = Client.objects.get(id=id)
            client.is_deleted = True

            client.save()
        
        return HttpResponseRedirect(reverse('compliance:client_index'))

    def deactivate(request, id):
        if (request.method == "POST"):
            client = Client.objects.get(id=id)
            client.is_active = False

            client.save()

        return HttpResponseRedirect(reverse('compliance:client_index'))

    def activate(request, id):
        if (request.method == "POST"):
            client = Client.objects.get(id=id)
            client.is_active = True

            client.save()

        return HttpResponseRedirect(reverse('compliance:client_index'))


class BirViews():
    """View functions of BIR sub-app"""
    def index(request):
        employee_list = Employee.objects.filter(is_deleted=False).order_by('abbr')
        paginator = Paginator(employee_list, 25)

        page = request.GET.get('page')
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
        }

        return render(request, 'employees/index.html', context)

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
        

class DeadlineViews():
    """View functions of Deadline sub-app"""
    def index(request):
        employee_list = Employee.objects.filter(is_deleted=False).order_by('abbr')
        paginator = Paginator(employee_list, 25)

        page = request.GET.get('page')
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
        }

        return render(request, 'employees/index.html', context)

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
