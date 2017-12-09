from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Q, Sum
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import datetime

from .dtr import compute_dtr, compute_dtr_latein, compute_dtr_absent, compute_dtr_ot, compute_dtr_night
from .forms import TimetableForm, ScheduleTimetableFormSet, LogForm, AttendanceForm, AttendanceLogFormSet, ProcessDTRFormset
from .models import Timetable, Schedule, Log, Attendance, AttendanceLog
from leaves.models import Application, Issuance

# Create your views here.


class DTRViews():
    """"""
    def index(request):
        return render(request, 'dtr/index.html')

    def dtr(request):
        if request.method == 'GET':
            return render(request, 'dtr/process-dtr.html', {'form': ProcessDTRFormset})

        else:
            employee_ids = ProcessDTRFormset(request.POST).cleaned_data
            date_from = request.POST.get('date_from')
            date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
            date_to = request.POST.get('date_to')
            date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()
            data = []

            # loop through employees
            for emp in employee_ids:
                if not emp:
                    break
                employee_id = emp['employee_id']
                # loop through dates
                temp_date = date_from
                while temp_date <= date_to:
                    schedule = Schedule.objects.filter(employee=employee_id, date=temp_date).first()
                    # check if no schedule, THEN skip
                    if not schedule:
                        # increase temp_date
                        temp_date += datetime.timedelta(days=1)
                        continue

                    schedule_timetables = schedule.scheduletimetable_set.all()
                    # loop through schedule timetables
                    for schedule_timetable in schedule_timetables:
                        # compute dtr
                        dtr = compute_dtr(employee_id, schedule_timetable, Log)
                        final_date_time_in = dtr['data'].get('final_date_time_in', None)
                        final_date_time_out = dtr['data'].get('final_date_time_out', None)
                        minutes_latein_actual = dtr['data'].get('late_in', 0)
                        minutes_late_in = minutes_latein_actual
                        minutes_early_out = dtr['data'].get('early_out', 0)
                        is_absent = dtr['data'].get('is_absent', False)
                        hours_deducted = 0
                        hours_paid = 0
                        application_id = None             
                        minutes_night_premium = 0
                        minutes_ot_premium = 0

                        # check if late_in is GREATER than 0 OR not empty
                        if minutes_latein_actual:
                            # compute_dtr_latein
                            dtr_late_in = compute_dtr_latein(employee_id, schedule_timetable, minutes_latein_actual, AttendanceLog)
                            minutes_late_in = dtr_late_in['data'].get('minutes_late_in', 0)

                        # check if absent
                        if is_absent:
                            application = Application.objects.filter(employee=employee_id, date=temp_date).first()
                            leave_application = {}
                            if application:
                                leave_type = application.leave
                                issued_hours = Issuance.objects.filter(employee=employee_id, valid_on_year=temp_date.year, leave=leave_type)\
                                    .aggregate(Sum('hours'))['hours__sum']    
                                availed_hours = Application.objects.filter(employee=employee_id, date__year=temp_date.year,\
                                     date__lte=temp_date).aggregate(Sum('paid_hours'))['paid_hours__sum']

                                leave_application = {
                                    'id': application.id,
                                    'issued_hours': issued_hours,
                                    'availed_hours': availed_hours,
                                    'charge_to_issuances': application.charge_to_issuances,
                                }
                            dtr_absent = compute_dtr_absent(schedule_timetable, leave_application=leave_application)
                            is_absent = dtr_absent['data'].get('is_absent', False)
                            hours_deducted = dtr_absent['data'].get('hours_deducted', 0)
                            hours_paid = dtr_absent['data'].get('hours_paid', 0)
                            application_id = dtr_absent['data'].get('leave_application_id', None)

                        # check if timetable is OT
                        if schedule_timetable.timetable.is_ot:
                            dtr_ot = compute_dtr_ot(schedule_timetable, minutes_late_in, minutes_early_out)
                            minutes_ot_premium = dtr_ot['data'].get('minutes_ot_premium', 0)

                        if not is_absent and final_date_time_in and final_date_time_out:
                            dtr_night = compute_dtr_night(schedule.date, final_date_time_in, final_date_time_out)
                            minutes_night_premium = dtr_night['data'].get('minutes_night_premium', 0)
                        
                        # post to dtr INTO AttendanceLog
                        _data = {
                            'final_date_time_in': final_date_time_in,
                            'final_date_time_out': final_date_time_out,
                            'minutes_latein_actual': minutes_latein_actual,
                            'minutes_late_in': minutes_late_in,
                            'minutes_early_out': minutes_early_out,
                            'is_absent': is_absent,
                            'hours_deducted': hours_deducted,
                            'hours_paid': hours_paid,
                            'application_id': application_id,
                            'minutes_night_premium': minutes_night_premium,
                            'minutes_ot_premium': minutes_ot_premium,
                        }
                        data.append(_data)

                        # increase temp_date
                        temp_date += datetime.timedelta(days=1)

            return HttpResponse(data)



class TimetableViews():

    def index(request, model_vars):
        q = request.GET.get('q')
        page = request.GET.get('page')

        # if search query is BLANK or NULL
        if not q:
            timetable_list = Timetable.objects.all().order_by( *model_vars.model_order_by )
        else:
            timetable_list = Timetable.objects.filter(remarks__contains=q).order_by( *model_vars.model_order_by )[:10]

        paginator = Paginator(timetable_list, 10)

        try:
            timetables = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            timetables = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            timetables = paginator.page(paginator.num_pages)

        context = {
            'model_list': timetables,
            'page': page,
            'q': q,
            'index_url': model_vars.model_url_index,
            'search_placeholder': model_vars.context_search_placeholder,
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
                messages.success(request, 'successfully created timetable ' + str(new_record.time_in) + ' - ' + str(new_record.time_out) + '.')
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
                    form.save()
                else:    
                    return fail

            if request.POST.get('save'):
                return HttpResponseRedirect(reverse(model_vars.model_url_index))
            else:
                # save and continue
                return HttpResponseRedirect(reverse(model_vars.model_url_detail, args=(id,)))

    def destroy(request, model_vars, id):
        record = model_vars.model.objects.get(id=id)
        record.delete()

        return HttpResponseRedirect(reverse(model_vars.model_url_index))


class ScheduleViews():

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
        formset_1 = ScheduleTimetableFormSet(instance=record)


        context = {
            'form' : form,
            'formset_1': formset_1,
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
                messages.success(request, 'successfully created ' + model_vars.model_name+ ' of ' + str(new_record.employee.abbr) + ' on ' + str(new_record.date) + '.')
            else:
                return fail

            return HttpResponseRedirect(reverse(model_vars.model_url_index))

    def update(request, model_vars, id):
        if request.method == 'POST':
            record = get_object_or_404(model_vars.model, pk=id)
            form = model_vars.model_form(request.POST, instance=record)
            formset_1 = ScheduleTimetableFormSet(request.POST, instance=record)
            
            context = {
                'form' : form,
                'record': record,
                'formset_1': formset_1,

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
                    form.save()
                else:    
                    return fail

            if formset_1.has_changed():
                if formset_1.is_valid():
                    formset_1.save()
                else:    
                    return fail

            if request.POST.get('save'):
                return HttpResponseRedirect(reverse(model_vars.model_url_index))
            else:
                # save and continue
                return HttpResponseRedirect(reverse(model_vars.model_url_detail, args=(id,)))

    def destroy(request, model_vars, id):
        record = model_vars.model.objects.get(id=id)
        record.delete()

        return HttpResponseRedirect(reverse(model_vars.model_url_index))


class LogViews():

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
                messages.success(request, 'successfully created ' + model_vars.model_name+ ' of ' + str(new_record.employee.abbr) + ' on ' + str(new_record.date_time) + '.')
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

            messages.success(request, 'successfully UPDATED ' + model_vars.model_name+ ' of ' + str(new_record.employee.abbr) + ' on ' + str(new_record.date_time) + '.')
            
            if request.POST.get('save'):
                return HttpResponseRedirect(reverse(model_vars.model_url_index))
            else:
                # save and continue
                return HttpResponseRedirect(reverse(model_vars.model_url_detail, args=(id,)))

    def destroy(request, model_vars, id):
        record = model_vars.model.objects.get(id=id)
        deleted_abbr = record.employee.abbr
        deleted_datetime = record.date_time
        record.delete()
        messages.warning(request, 'successfully DELETED ' + model_vars.model_name+ ' of ' + str(deleted_abbr) + ' on ' + str(deleted_datetime) + '.')
        return HttpResponseRedirect(reverse(model_vars.model_url_index))


class AttendanceViews():

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

        formset_1 = AttendanceLogFormSet(instance=record)
        


        context = {
            'form' : form,
            'record': record,
            'formset_1': formset_1,
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
                messages.success(request, 'successfully created ' + model_vars.model_name+ ' of ' + str(new_record.employee.abbr) + ' on ' + str(new_record.date) + '.')
            else:
                return fail

            return HttpResponseRedirect(reverse(model_vars.model_url_index))

    def update(request, model_vars, id):
        if request.method == 'POST':
            record = get_object_or_404(model_vars.model, pk=id)
            form = model_vars.model_form(request.POST, instance=record)
            formset_1 = AttendanceLogFormSet(request.POST, instance=record)
            
            context = {
                'form' : form,
                'formset_1': formset_1,
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

            if formset_1.has_changed():
                if formset_1.is_valid():
                    formset_1.save()

            messages.success(request, 'successfully UPDATED ' + model_vars.model_name + ' of ' + record.employee.abbr)
            
            if request.POST.get('save'):
                return HttpResponseRedirect(reverse(model_vars.model_url_index))
            else:
                # save and continue
                return HttpResponseRedirect(reverse(model_vars.model_url_detail, args=(id,)))

    def destroy(request, model_vars, id):
        record = model_vars.model.objects.get(id=id)
        deleted_abbr = record.employee.abbr
        deleted_date = record.date
        record.delete()
        messages.warning(request, 'successfully DELETED ' + model_vars.model_name+ ' of ' + str(deleted_abbr) + ' on ' + str(deleted_date) + '.')
        return HttpResponseRedirect(reverse(model_vars.model_url_index))

class GraceLateInViews():

    def index(request, model_vars):
        q = request.GET.get('q')
        page = request.GET.get('page')

        # if search query is BLANK or NULL
        if not q:
            record_list = model_vars.model.objects.all()
        else:
            record_list = model_vars.model.objects.filter(Q(alias__contains=q) | Q(remarks__contains=q))[:10]

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
                messages.success(request, 'successfully CREATED ' + model_vars.model_name+ ' with ' + str(new_record.alias) + '.')
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

            messages.success(request, 'successfully UPDATED ' + model_vars.model_name+ ' with ' + str(new_record.alias) + '.')
            
            if request.POST.get('save'):
                return HttpResponseRedirect(reverse(model_vars.model_url_index))
            else:
                # save and continue
                return HttpResponseRedirect(reverse(model_vars.model_url_detail, args=(id,)))

    def destroy(request, model_vars, id):
        record = model_vars.model.objects.get(id=id)
        deleted_abbr = record.alias
        record.delete()
        messages.warning(request, 'successfully DELETED ' + model_vars.model_name+ ' with ' + str(deleted_abbr) + '.')
        return HttpResponseRedirect(reverse(model_vars.model_url_index))

