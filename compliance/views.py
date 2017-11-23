from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.forms import model_to_dict

# pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Client, ClientPractitioner, BirCompliance, BirDeadline, DeadlineStatus
from employees.models import Employee
from contacts.models import Contact

# forms
from .forms import ClientForm, PractitionerFormSet, BIRComplianceFormSet


class ComplianceViews():
    """View functions of Compliance main-app"""
    def index(request):
        return render(request, 'compliance/index.html')


class ClientViews():
    """View functions of Client sub-app"""
    def index(request):
        q = request.GET.get('q')
        page = request.GET.get('page')

        if not q:
            q = ''
            client_list = Client.objects.filter(contact__alias__contains=q).order_by('date_start')
        else:
            client_list = Client.objects.filter(contact__alias__contains=q).order_by('date_start')[:10]

        paginator = Paginator(client_list, 25)

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
            'page': page,
            'q': q,
            'index_url': 'compliance:client_index',
            'search_placeholder': 'type client alias'
        }

        return render(request, 'compliance/clients/index.html', context)

    def detail(request, id):
        model = get_object_or_404(Client, pk=id)

        form = ClientForm(
            instance=model,
            initial=model_to_dict(model),
        )

        formset_practitioner = PractitionerFormSet(instance=model)
        formset_bir = BIRComplianceFormSet(instance=model)


        context = {
            'form' : form,
            'model': model,
            'str_model_id': str(model.id),
            'formset_practitioner': formset_practitioner,
            'formset_bir': formset_bir,
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
                form = ClientForm(initial={'contact':  contact})
            else:
                form = ClientForm()
                
            context = {
                'form' : form,
            }

            return render(request, 'compliance/clients/new.html', context)
        else:
            return HttpResponseRedirect(reverse('compliance:client_index'))

    def create(request):
        if request.method == "POST":
            # validate form
            form = ClientForm(request.POST)
            
            context = {
                'form' : form,
            }

            fail = render(request, 'compliance/clients/new.html', context)

            if form.is_valid():
                new_client = form.save()
            else:
                return fail

            return HttpResponseRedirect(reverse('compliance:client_detail', args=[new_client.id,]))

    def update(request, id):
        if request.method == 'POST':
            client = get_object_or_404(Client, pk=id)
            form = ClientForm(request.POST, instance=client)
            formset_practitioner = PractitionerFormSet(request.POST, instance=client)
            formset_bir = BIRComplianceFormSet(request.POST, instance=client)
            
            context = {
                'form' : form,
                'model': client,
                'formset_practitioner': formset_practitioner,
                'formset_bir': formset_bir,
            }

            fail = render(request, 'compliance/clients/detail.html', context)

            if form.has_changed():
                if form.is_valid():
                    form.save()
                else:    
                    return fail
            if formset_practitioner.has_changed():
                if formset_practitioner.is_valid():
                    formset_practitioner.save()
                else:    
                    return fail

            if formset_bir.has_changed():
                if formset_bir.is_valid():
                    formset_bir.save()
                else:    
                    return fail

            return HttpResponseRedirect(reverse('compliance:client_index'))

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
        bir_list = BirDeadline.objects.all()
        paginator = Paginator(bir_list, 25)

        page = request.GET.get('page')
        try:
            bir = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            bir = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            bir = paginator.page(paginator.num_pages)

        context = {
            'bir_list': bir,
        }

        return render(request, 'compliance/bir/index.html', context)

    def destroy(request, id):
        employee = Employee.objects.get(id=id)
        employee.is_deleted = True

        employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
        

class StatusViews():
    """View functions of Status sub-app"""
    def index(request):
        status_list = DeadlineStatus.objects.filter(is_deleted=False).order_by('as_of')
        paginator = Paginator(status_list, 25)

        page = request.GET.get('page')
        try:
            status = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            status = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            status = paginator.page(paginator.num_pages)

        context = {
            'status_list': status,
        }

        return render(request, 'compliance/status/index.html', context)

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
