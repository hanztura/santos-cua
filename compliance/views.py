from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.forms import model_to_dict
from django.db.models import Q
from django.core import serializers
import datetime
import calendar

# pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Client, ClientPractitioner, BirCompliance, BirDeadline, DeadlineStatus, ClientAttachment
from employees.models import Employee
from contacts.models import Contact
from bir.models import BirForm, BirFormSchedule

# forms
from .forms import ClientForm, ClientAttachmentForm, PractitionerFormSet, BIRComplianceFormSet



def create_bir_deadline(client_bir, date_deadline, date_notify_start):
    deadline = BirDeadline(compliance=client_bir, date_deadline=date_deadline, date_notify_start=date_notify_start)
    deadline.save()

def create_bir_deadlines(client_object, client_bir_compliances):
    # client_bir_compliances = new_client_bir
    def get_month_value(bus_year_end_on, period_type):
        """
            returns INT
            convert bir compliance schedule index into month values
            based on their business year
        """
        period_type_multipliers = {
            'M': 1,
            'Q': 3,
        }
        _temp = bus_year_end_on + (period_type_multipliers[period_type] * i)
        _temp = (_temp % 12)
        if (_temp % 12) == 0:
            _temp = 12

        return _temp


    date_start = client_object.date_start
    date_end = client_object.date_end
    client = Client.objects.get(pk=client_object.id)
    client_bye = client.month_business_year_end

    period_ref = {
        # monthly
        'M': (),

        # quarterly
        'Q': (),

        # annually
        'A': (),
    }

    if client.is_calendar_year:
        period_ref['M'] = ('monthly', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        period_ref['Q'] = ('quarterly', 3, 6, 9, 12)
        period_ref['A'] = ('annually', 12)
    else:
        # if client is NOT calendar year
        for k, v in period_ref.items():
            if k == 'M':
                temp = ['monthly']
                for i in range(1,13):
                    temp.append(get_month_value(client_bye, k))
                    period_ref['M'] = tuple(temp)
                    continue

            if k == 'Q':
                temp = ['quarterly']
                for i in range(1,5):
                    temp.append(get_month_value(client_bye, k))
                    period_ref['Q'] = tuple(temp)
                    continue

            if k == 'A':
                temp = ['annually']
                # month end of the annual
                temp.append(client_bye)
                period_ref['A'] = tuple(temp)
                continue

    # loop through client's years between date_start AND date_end
    for year in range(date_start.year-1, date_end.year+1):
        # loop through client bir compliance
        for client_bir in client_bir_compliances:
            bir_form = BirForm.objects.get(pk=client_bir.bir_form_id)
            bir_form_schedules = bir_form.schedules.all().order_by('index')

            form_deadline_period = bir_form.dead_period #uppercase M, Q, A, C
            form_bus_year_ref = bir_form.dead_by_ref #uppercase A = absolute, R = relative
            form_deadline_date_type = bir_form.dead_date_type #uppercase F = fixed, C = count

            
            # loop through the form's schedules (index)
            for schedule in list(bir_form_schedules):
                # if form schedule is Absolute meaning schedule.index 1 = January ... 12 = December
                if form_bus_year_ref == 'A':
                    temp_period_ref = {
                        # monthly
                        'M': ('monthly', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),

                        # quarterly
                        'Q': ('quarterly', 3, 6, 9, 12),

                        # annually
                        'A': ('annually', 12),
                    }
                    # convert schedule index into actual month value like 1 = january ... 12 = december
                    month_value_of_index = temp_period_ref[form_deadline_period][schedule.index]

                elif form_bus_year_ref == 'R':
                    # convert schedule index into actual month value like 1 = january ... 12 = december
                    month_value_of_index = period_ref[form_deadline_period][schedule.index]

                # if deadline date determination is fix
                if form_deadline_date_type == 'F':
                    deadline_month = month_value_of_index + schedule.month # todo: change schedule.index into something that will lookup the actual month equivalent of the index
                    deadline_year = int(deadline_month / 12)

                    if (deadline_month % 12) == 0:
                        deadline_month = 12
                        deadline_year = deadline_year - 1
                    else:
                        deadline_month = deadline_month % 12

                    # create/determine: date_deadline
                    date_deadline = datetime.date(year + deadline_year, deadline_month, schedule.day)

                # if deadline date determination is count
                elif form_deadline_date_type == 'C':
                    deadline_year = year
                    deadline_month = month_value_of_index
                    deadline_day = calendar.monthrange(deadline_year, deadline_month)[1]

                    date_deadline = datetime.date(deadline_year, deadline_month, deadline_day)
                    # days
                    date_deadline = date_deadline + datetime.timedelta(days=schedule.day)

                if date_start <= date_deadline <= date_end:
                    # create a bir deadline
                    date_notify_start = date_deadline - datetime.timedelta(days=20)
                    deadline = create_bir_deadline(client_bir, date_deadline, date_notify_start)

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
            client_list = Client.objects.filter(contact__alias__contains=q).order_by('date_start')[:20]

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

        formset_practitioner = PractitionerFormSet(instance=model,)
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
        # id parameter is used when creating a record is from other views
        if request.method == "GET":
            if ((not id == 0) and (not id == None)):
                contact = Contact.objects.get(pk=id)
                form = ClientForm(initial={'contact':  contact})
            else:
                form = ClientForm()
            
            formset_practitioner = PractitionerFormSet()
            formset_bir = BIRComplianceFormSet()
            formset_bir.extra = 1
                
            context = {
                'form' : form,
                'formset_practitioner': formset_practitioner,
                'formset_bir': formset_bir,
            }

            return render(request, 'compliance/clients/new.html', context)
        else:
            return HttpResponseRedirect(reverse('compliance:client_index'))

    def create(request):
        if request.method == "POST":
            # validate form
            form = ClientForm(request.POST)
            formset_practitioner = PractitionerFormSet(request.POST)
            formset_bir = BIRComplianceFormSet(request.POST)
            
            context = {
                'form' : form,
                'formset_practitioner': formset_practitioner,
                'formset_bir': formset_bir,
            }

            fail = render(request, 'compliance/clients/new.html', context)

            if form.is_valid():
                new_client = form.save()
                formset_practitioner.instance = new_client

            else:
                return fail
            
            if formset_practitioner.is_valid():
                formset_bir.instance = new_client

            else:
                formset_practitioner.instance = None
                new_client.delete()
                return fail

            if formset_bir.is_valid():
                new_client_practitioners = formset_practitioner.save()
                new_client_bir = formset_bir.save()

            else:
                formset_practitioner.instance = None
                formset_bir.instance = None

                new_client_practitioners.delete()
                new_client.delete()

                return fail

            # before return, create bir deadlines
            create_bir_deadlines(new_client, new_client_bir)

            # data = serializers.serialize('json', bir_form)
            # return HttpResponse(date_start, content_type='application/json')


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
            # client.is_deleted = True

            # client.save()
            client.delete()

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
        q = request.GET.get('q')
        page = request.GET.get('page')
        user = request.user

        months = {
            'jan': 1,
            'feb': 2,
            'mar': 3,
            'apr': 4,
            'may': 5,
            'jun': 6,
            'jul': 7,
            'aug': 8,
            'sep': 9,
            'oct': 10,
            'nov': 11,
            'dec': 12,
        }

        if not q:
            q = ''
            bir = BirDeadline.objects.filter(is_deleted=False).order_by('date_deadline')
            bir = [x for x in bir if (x.practitioner.user == user or (user == x.practitioner.supervisors.user)) ]
        else:
            _q = q.lower()
            if _q.startswith(':') and (not _q.startswith('::')):
                bir = BirDeadline.objects.filter(is_deleted=False).filter(date_deadline__month=months[_q[1:]]).order_by('date_deadline')[:10]
                bir = [x for x in bir if (x.practitioner.user == user or (user == x.practitioner.supervisors.user)) ] # practitioner only
            elif _q.startswith('::'):
                bir = BirDeadline.objects.filter(is_deleted=False).order_by('date_deadline')[:10]
                bir = [x for x in bir if (x.practitioner.user == user or (user == x.practitioner.supervisors.user)) ] # practitioner only
                bir = [x for x in bir if (x.practitioner.abbr == _q[2:]) ]
            else:
                bir = BirDeadline.objects.filter(is_deleted=False).filter(Q(compliance__client__contact__alias__contains=q) | Q(compliance__bir_form__form_code__contains=q)).order_by('date_deadline')[:10]
            

        paginator = Paginator(bir, 25)

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
            'page': page,
            'q': q,
            'index_url': 'compliance:bir_index',
            'search_placeholder': 'type client alias or bir form',
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


class AttachmentViews():
    """
        compliance client/engagements attachments
    """

    def index(request, client_id):
        client = Client.objects.get(pk=client_id)
        q = request.GET.get('q')
        page = request.GET.get('page')

        if not q:
            q = ''
            attachment_list = client.attachments.filter(code__contains=q)
        else:
            attachment_list = client.attachments.filter(code__contains=q)[:10]


        paginator = Paginator(attachment_list, 25)

        try:
            attachments = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            attachments = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            attachments = paginator.page(paginator.num_pages)

        context = {
            'attachments': attachments,
            'client': client,
            'page': page,
            'q': q,
            'index_url': 'compliance:attachment_index',
            'search_placeholder': 'type attachment code',
        }

        return render(request, 'compliance/attachments/index.html', context)

    def new(request, client_id=0):
        # id parameter is used when creating a record is from other views
        if request.method == "GET":
            if ((not client_id == 0) and (not client_id == None)):
                client = Client.objects.get(pk=client_id)
                form = ClientAttachmentForm(initial={'client': client})
            else:
                form = ClientAttachmentForm()
                
            context = {
                'form' : form,
            }

            return render(request, 'compliance/attachments/new.html', context)
        else:
            return HttpResponseRedirect(reverse('compliance:client_index'))

    def create(request):
        if request.method == "POST":
            # validate form
            form = ClientAttachmentForm(request.POST, request.FILES)
            
            context = {
                'form' : form,
            }

            fail = render(request, 'compliance/attachments/new.html', context)

            if form.is_valid():
                new_attachment = form.save()
            else:
                return fail

            return HttpResponseRedirect(reverse('compliance:attachment_index', new_attachment.client_id))

    def destroy(request, id):
        if (request.method == "POST"):
            attachment = ClientAttachment.objects.get(id=id)
            attachment.delete()

        return HttpResponseRedirect(reverse('compliance:attachment_index'))
        