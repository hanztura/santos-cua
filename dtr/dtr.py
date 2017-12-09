import datetime
from django.db.models import Q, Sum

from .models import Schedule, Log, Attendance, AttendanceLog
from employees.models import Employee

def compute_dtr(employee, schedule_timetable, LogModel):
    ret = {
        'fields': (
            'schedule_timetable_id',
            'final_date_time_in',
            'final_date_time_out',
            'is_absent',
            'late_in',
            'early_out',
            'ot_hours',
            'ot_premium_hours',
            'log_id_out',
            'log_id_in',
        ),

        'data': {}
    }

    # schedule variables
    schedule_timetable_id = schedule_timetable.id
    date = schedule_timetable.schedule.date

    # threshold minutes
    minutes_threshold_early_in = schedule_timetable.minutes_threshold_early_in
    minutes_threshold_late_in = schedule_timetable.minutes_threshold_late_in
    minutes_threshold_early_out = schedule_timetable.minutes_threshold_early_out
    minutes_threshold_late_out = schedule_timetable.minutes_threshold_late_out

    # schedule datetime
    datetime_inout = schedule_timetable.get_datetime_inout
    schedule_datetime_in = datetime_inout['in']
    schedule_datetime_out = datetime_inout['out']

    # schedule datetime THRESHOLDS
    if schedule_datetime_in:
        threshold_datetime_early_in = schedule_datetime_in - datetime.timedelta(minutes=minutes_threshold_early_in)
        threshold_datetime_late_in = schedule_datetime_in + datetime.timedelta(minutes=minutes_threshold_late_in)
    else:
        threshold_datetime_early_in = None
        threshold_datetime_late_in = None

    if schedule_datetime_out:
        threshold_datetime_early_out = schedule_datetime_out - datetime.timedelta(minutes=minutes_threshold_early_out)
        threshold_datetime_late_out = schedule_datetime_out + datetime.timedelta(minutes=minutes_threshold_late_out)
    else:
        threshold_datetime_early_out = None
        threshold_datetime_late_out = None

    # select logs with appropriate filters
    logs_filtered = LogModel.objects.filter(employee=employee, is_used=False, date_time__range=(threshold_datetime_early_in, threshold_datetime_late_out)).order_by('date_time', 'log_type')

    is_ot = schedule_timetable.timetable.is_ot
    is_absent = True
    final_date_time_in = None
    final_date_time_out = None
    late_in = 0
    log_id_in = 0
    log_id_out  = 0     

    if logs_filtered.exists():
        logs_filtered_in = logs_filtered.filter(Q(log_type=2) | Q(date_time__range=(
            threshold_datetime_early_in,
            threshold_datetime_late_in))
        )

        logs_filtered_out = logs_filtered.filter(Q(log_type=3) | Q(date_time__range=(
            threshold_datetime_early_out,
            threshold_datetime_late_out))
        )

        # means there are logs BOTH in/out
        if logs_filtered_in.exists() or logs_filtered_out.exists():
            is_absent = False
        # means there are NO logs BOTH in/out within THRESHOLDS
        else:
            # end process and return absent data
            data = {
                'schedule_timetable_id': schedule_timetable_id,
                'final_date_time_in': None,
                'final_date_time_out': None,
                'is_absent': True,
                'late_in': 0,
                'early_out': 0,
                'ot_hours': 0,
                'ot_premium_hours': 0,
                'log_id_in': None,
                'log_id_out': None,
            }

            ret['data'] = data
            return ret

        # loop through logs and try to assign into schedule timetables AS attendance item
        log_datetimes = {
            'fields': ('log_id', 'log_datetime_cleaned', 'log_type', 'timedelta'),
            'data_in': {}, # dict values
            'data_out': {},
        }

        # loop through logs_in
        for log in logs_filtered_in:
            log_datetime_cleaned = log.date_time.replace(second=0, microsecond=0, tzinfo=None) # round down to nearest minute

            if (not log_datetimes['data_in']) or (log_datetime_cleaned < log_datetimes['data_in']['log_datetime_cleaned']) :
                log_timedelta = schedule_datetime_in - log_datetime_cleaned
                data = {
                    'log_id': log.id,
                    'log_datetime_cleaned': log_datetime_cleaned,
                    'log_type': 2, # IN
                    'timedelta': log_timedelta,
                }
                log_datetimes['data_in'] = data # set to log_datetimes

        # lopp through logs_out
        for log in logs_filtered_out:
            log_datetime_cleaned = log.date_time.replace(second=0, microsecond=0, tzinfo=None) # round down to nearest minute

            if (not log_datetimes['data_out']) or (log_datetime_cleaned > log_datetimes['data_out']['log_datetime_cleaned']):
                log_timedelta = log_datetime_cleaned - schedule_datetime_out
                data = {
                    'log_id': log.id,
                    'log_datetime_cleaned': log_datetime_cleaned,
                    'log_type': 3, # OUT
                    'timedelta': log_timedelta,
                }
                log_datetimes['data_out'] = data # set to log_datetimes

        data = {
            'schedule_timetable_id': schedule_timetable_id,
            'final_date_time_in': None,
            'final_date_time_out': None,
            'is_absent': False,
            'late_in': schedule_timetable.timetable.hours_paid / 2,
            'early_out': schedule_timetable.timetable.hours_paid / 2,
            'ot_hours': 0,
            'ot_premium_hours': 0,
            'log_id_in': None,
            'log_id_out': None,
        }

        # refine log_datetimes and set to return value
        # log_in
        if log_datetimes['data_in']:
            log_datetime_in = log_datetimes['data_in']
            
            data['log_id_in'] = log_datetime_in['log_id']

            # if NOT late in
            if log_datetime_in['timedelta'].days >= 0:
                data['final_date_time_in'] = schedule_datetime_in
                data['late_in'] = 0
            # if late in
            else:
                data['final_date_time_in'] = log_datetime_in['log_datetime_cleaned']
                data['late_in'] = (86400 - log_datetime_in['timedelta'].seconds) / 60 # convert timedelta seconds into minutes

        # log_out
        if log_datetimes['data_out']:
            log_datetime_out = log_datetimes['data_out']
            
            data['log_id_out'] = log_datetime_out['log_id']
            
            # if not early out
            if log_datetime_out['timedelta'].days >= 0:
                data['final_date_time_out'] = schedule_datetime_out
                data['early_out'] = 0
            else:
                data['final_date_time_out'] = log_datetime_out['log_datetime_cleaned']
                data['early_out'] = (86400 - log_datetime_out['timedelta'].seconds) / 60 # convert timedelta seconds into minutes

        ret['data'] = data
    # if NO logs at all for this schedule_timetable
    else:
        # end process and return absent data
        data = {
            'schedule_timetable_id': schedule_timetable_id,
            'final_date_time_in': None,
            'final_date_time_out': None,
            'is_absent': True,
            'late_in': 0,
            'early_out': 0,
            'ot_hours': 0,
            'ot_premium_hours': 0,
            'log_id_in': None,
            'log_id_out': None,
        }

        ret['data'] = data
        
    return ret

def compute_dtr_latein(employee_id, schedule_timetable, late_in, AttendanceLogModel):
    # CURRENTLY, simple value type of grace period
    ret = {
        'fields': (
            'schedule_timetable_id',
            'minutes_latein_actual',
            'minutes_late_in',
        ),
        'data': {}
    }

    schedule_date = schedule_timetable.schedule.date
    timetable_grace = schedule_timetable.timetable.grace_late_in
    # check if grace is NOT null
    if timetable_grace:
        grace_type = timetable_grace.grace_type
        grace_sub_type = timetable_grace.grace_sub_type
        value_minutes = timetable_grace.value_minutes
        value_type = timetable_grace.value_type
    # if no grace period, end process and return default values
    else:
        data = {
            'schedule_timetable_id': schedule_timetable.id,
            'minutes_latein_actual': late_in,
            'minutes_late_in': late_in,
        }

        ret['data'] = data
        return ret

    if grace_type == 1: # grace type INSTANCE
        if value_type == 1: # simple
            if late_in > value_minutes:
                minutes_late_in = late_in - value_minutes
            else:
                minutes_late_in = 0

            data = {
                'schedule_timetable_id': schedule_timetable.id,
                'minutes_latein_actual': late_in,
                'minutes_late_in': minutes_late_in,
            }

            ret['data'] = data
            return ret

        else: # complex TEMPORARY
            data = {
                'schedule_timetable_id': schedule_timetable.id,
                'minutes_latein_actual': late_in,
                'minutes_late_in': late_in,
            }

            ret['data'] = data
            return ret
            
    elif grace_type == 2: # grace type PERIODIC
        if value_type == 1: # simple
            period_type = schedule_timetable.timetable.grace_late_in.grace_sub_type
            if period_type == 1: # daily
                periodic_late_actual = AttendanceLogModel.objects.filter(
                    attendance__date=schedule_date,
                    attendance__employee_id=employee_id).aggregate(Sum('minutes_late_in_actual')).get('minutes_late_in_actual__sum', 0)
            elif period_type == 2: # monthly
                periodic_late_actual = AttendanceLogModel.objects.filter(
                    attendance__date__month=schedule_date.month,
                    attendance__employee_id=employee_id).aggregate(Sum('minutes_late_in_actual')).get('minutes_late_in_actual__sum', 0)
            
            if not periodic_late_actual:
                periodic_late_actual = 0

            # check if accumulated actual late minutes is  BEYOND allowed grace period
            if periodic_late_actual >= value_minutes:
                data = {
                    'schedule_timetable_id': schedule_timetable.id,
                    'minutes_latein_actual': late_in,
                    'minutes_late_in': late_in,
                }

                ret['data'] = data
                return ret
            else:
                value_minutes_remaining = value_minutes - periodic_late_actual
                # if CURRENT actual minutes late is BIGGER or EQUAL to grace minutes remaing
                if late_in >= value_minutes_remaining:
                    minutes_late_in = late_in - value_minutes_remaining
                # if current actual minutes late is LESS than grace minutes remaing
                else:
                    minutes_late_in = 0

                data = {
                    'schedule_timetable_id': schedule_timetable.id,
                    'minutes_latein_actual': late_in,
                    'minutes_late_in': minutes_late_in,
                }

                ret['data'] = data
                return ret

        else: # complex TEMPORARY
            data = {
                'schedule_timetable_id': schedule_timetable.id,
                'minutes_latein_actual': late_in,
                'minutes_late_in': late_in,
            }

            ret['data'] = data
            return ret

def compute_dtr_absent(schedule_timetable, leave_application = {}):
    # returns the following values
    ret = {
        'fields': ['is_absent', 'hours_deducted', 'hours_paid', 'leave_application_id'],
        'data': {}
    }

    date = schedule_timetable.schedule.date
    schedule = schedule_timetable.schedule
    employee = schedule.employee
    schedule_hours_paid = schedule_timetable.timetable.hours_paid

    # check if restday
    if schedule.is_rest_day:
        data = {
            'is_absent': False,
            'hours_deducted': 0,
            'hours_paid': 0,
            'leave_application_id': None,
        }
    # if NOT restday
    else:
        # set employee_branch assigned
        # branch assigned is set on employee schedule_timetable
        employee_project = schedule_timetable.sub_project
        employee_branch = employee_project.branch
        while not employee_branch:
            employee_project = employee_project.parent
            employee_branch = employee_project.branch

        # determine holiday
        employee_branch_city = employee_branch.city
        holiday = employee_branch_city.holiday_set.filter(date=date).first()
        if holiday:
            # determine if holiday is PAY on absent
            if holiday.pay_on_absent:
                data = {
                    'is_absent': True,
                    'hours_deducted': 0,
                    'hours_paid': schedule_hours_paid,
                    'leave_application_id': None,
                }
            # if NOT pay on absent
            else:
                data = {
                    'is_absent': True,
                    'hours_deducted': schedule_hours_paid,
                    'hours_paid': 0,
                    'leave_application_id': None,
                }
        # if NOT holiday
        else:
            # determine if ON leave
            if leave_application:
                issued_hours = leave_application['issued_hours']
                availed_hours = leave_application['availed_hours']
                available_hours = issued_hours - availed_hours
                # determine if there is still available leave credits
                if leave_application['charge_to_issuances'] and available_hours > 0:
                    # determine if available hours is LESS than hours absent
                    if available_hours < schedule_hours_paid:
                        data = {
                            'is_absent': True,
                            'hours_deducted': schedule_hours_paid - available_hours,
                            'hours_paid': available_hours,
                            'leave_application_id': leave_application['id'],
                        }
                    # if available hours is MORE or EQUAL to hours absent THEN hours_deducted is auto ZERO
                    else:
                        data = {
                            'is_absent': True,
                            'hours_deducted': 0,
                            'hours_paid': schedule_hours_paid,
                            'leave_application_id': leave_application['id'],
                        }

                # if NOT charged to issuances OR there is NO available leave credits
                else:
                    data = {
                        'is_absent': True,
                        'hours_deducted': schedule_hours_paid,
                        'hours_paid': 0,
                        'leave_application_id': leave_application['id'],
                    }
            # if NOT on leave
            else:
                data = {
                    'is_absent': True,
                    'hours_deducted': schedule_hours_paid,
                    'hours_paid': 0,
                    'leave_application_id': None,
                }

    ret['data'] = data
    return ret

def compute_dtr_ot(schedule_timetable, late_in_minutes, early_out_minutes):
    # returns the following values
    ret = {
        'fields': ['minutes_ot_premium'],
        'data': {
            'minutes_ot_premium': 0,
        }
    }

    # determine if schedule_timetable is OT timetable
    if schedule_timetable.timetable.is_ot:
        schedule_ot_hours = schedule_timetable.timetable.hours_paid
        schedule_ot_mintues = int(schedule_ot_hours * 60) # round down to nearest integer
        actual_ot_minutes = schedule_ot_mintues - late_in_minutes, early_out_minutes
        data = {
            'minutes_ot_premium': actual_ot_minutes,
        }

        ret['data'] = data

    return ret

def compute_dtr_night(schedule_date, final_date_time_in, final_date_time_out,):
    # returns the following values
    ret = {
        'fields': ['minutes_night_premium'],
        'data': {
            'minutes_night_premium': 0,
            'message': '',
        }
    }

    # time_in_date = final_date_time_in.date
    # time_in_time = final_date_time_in.replace(second=0, microsecond=0).time

    # time_out_date = final_date_time_out.date
    # time_out_time = final_date_time_out.replace(second=0, microsecond=0).time

    datetime_night_in = datetime.datetime.combine(schedule_date, datetime.time(hour=22))
    datetime_nightout_today = datetime.datetime.combine(schedule_date, datetime.time(hour=6))
    datetime_nightout_tomorrow = datetime.datetime.combine(schedule_date + datetime.timedelta(days=1), datetime.time(hour=6))
    # determine if shift fall timein < 6AM today OR between 10PM AND Tomorrow 6AM
    if final_date_time_in < datetime_nightout_today:
        # check if actual time_out is > 06AM tomorrow
        if final_date_time_out > datetime_nightout_today:
            minutes_night_premium = datetime_nightout_today - final_date_time_in
        else:
            minutes_night_premium = final_date_time_out - final_date_time_in
    elif final_date_time_in >= datetime_night_in:
        # check if actual time_out is > 06AM tomorrow
        if final_date_time_out > datetime_nightout_tomorrow:
            minutes_night_premium = datetime_nightout_tomorrow - final_date_time_in
        else:
            minutes_night_premium = final_date_time_out - final_date_time_in

    elif final_date_time_out > datetime_night_in:
        # check if actual time_out is > 06AM tomorrow
        if final_date_time_out > datetime_nightout_tomorrow:
            minutes_night_premium = datetime_nightout_tomorrow - datetime_night_in
        else:
            minutes_night_premium = final_date_time_out - datetime_night_in
    else:
        return ret
    

    if minutes_night_premium.days < 0:
        return ret

    minutes_night_premium = (minutes_night_premium.seconds) / 60
    ret['data'] = { 'minutes_night_premium': minutes_night_premium,}
    return ret
