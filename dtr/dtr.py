import datetime
from django.utils import timezone
from django.db.models import Q

from .models import Schedule, Log, Attendance, AttendanceLog
from employees.models import Employee

def compute_dtr_2(employee, schedule_timetable, log_model):
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

        'data': []
    }

    schedule_timetable_id = schedule_timetable.id
    date = schedule_timetable.schedule.date
    sched_datetime = datetime.datetime(year=date.year, month=date.month, day=date.day) # convert date INTO datetime
    date_before = date - datetime.timedelta(days=1)
    date_after = date + datetime.timedelta(days=1)

    minutes_threshold_early_in = schedule_timetable.minutes_threshold_early_in
    minutes_threshold_late_in = schedule_timetable.minutes_threshold_late_in
    minutes_threshold_early_out = schedule_timetable.minutes_threshold_early_out
    minutes_threshold_late_out = schedule_timetable.minutes_threshold_late_out
    
    schedule_time_in = schedule_timetable.timetable.time_in
    schedule_time_out = schedule_timetable.timetable.time_out
    time_in_hours = schedule_time_in.hour # time in HOUR sample 08:30, this is 8
    time_in_minutes = schedule_time_in.minute # time in MINUTE sample 08:30, this is 30
    time_out_hours = schedule_time_out.hour # time in HOUR sample 18:00, this is 18
    time_out_minutes = schedule_time_out.minute # time in MINUTE sample 18:00, this is 0

    schedule_datetime_in = sched_datetime + datetime.timedelta(hours=time_in_hours, minutes=time_in_minutes)
    # check if time out falls on the next day
    if schedule_time_in >= schedule_time_out:
        time_out_hours = time_out_hours + 24
        schedule_datetime_out = sched_datetime + datetime.timedelta(hours=time_out_hours, minutes=time_out_minutes)
    else:
        schedule_datetime_out = sched_datetime + datetime.timedelta(hours=time_out_hours, minutes=time_out_minutes)

    threshold_datetime_early_in = schedule_datetime_in - datetime.timedelta(minutes=minutes_threshold_early_in)
    threshold_datetime_late_in = schedule_datetime_in + datetime.timedelta(minutes=minutes_threshold_late_in)
    threshold_datetime_early_out = schedule_datetime_out - datetime.timedelta(minutes=minutes_threshold_early_out)
    threshold_datetime_late_out = schedule_datetime_out + datetime.timedelta(minutes=minutes_threshold_late_out)

    logs_filtered = log_model.objects.filter(employee=employee, is_used=False, date_time__range=(threshold_datetime_early_in, threshold_datetime_late_out)).order_by('date_time', 'log_type')

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

        # means there are logs
        if logs_filtered_in.exists() or logs_filtered_out.exists():
            is_absent = False
        else:
            # end process and return null value
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
                log_timedelta = log_datetime_cleaned - schedule_datetime_in
                data = {
                    'log_id': log.id,
                    'log_datetime_cleaned': log_datetime_cleaned,
                    'log_type': 3, # OUT
                    'timedelta': log_timedelta,
                }
                log_datetimes['data_out'] = data # set to log_datetimes

        # for log in logs_filtered:
        #     # loop through logs
        #     log_datetime_cleaned = log.date_time.replace(second=0, microsecond=0, tzinfo=None) # round down to nearest minute

        #     if threshold_datetime_early_in <= log_datetime_cleaned <= threshold_datetime_late_in:
        #         # if log is within threshold of early_in AND late_in
        #         log_timedelta = schedule_datetime_in - log_datetime_cleaned
        #         data = {
        #             'log_id': log.id,
        #             'log_datetime_cleaned': log_datetime_cleaned,
        #             'log_type': 2, # IN
        #             'schedule_timetable_id': schedule_timetable_id,
        #             'timedelta': log_timedelta,
        #         }
        #         log_datetimes['data'].append(data) # append to log_datetimes

        #     elif threshold_datetime_early_out <= log_datetime_cleaned <= threshold_datetime_late_out:
        #         # if log is within threshold of early_out AND late_out
        #         log_timedelta = log_datetime_cleaned - schedule_datetime_out
        #         data = {
        #             'log_id': log.id,
        #             'log_datetime_cleaned': log_datetime_cleaned,
        #             'log_type': 3, # OUT
        #             'schedule_timetable_id': schedule_timetable_id,
        #             'timedelta': log_timedelta,
        #         }
        #         log_datetimes['data'].append(data) # append to log_datetimes


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
            
            # if not late in
            if log_datetime_in['timedelta'].days >= 0:
                data['final_date_time_in'] = schedule_datetime_in
                data['late_in'] = 0
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
                data['final_date_time_in'] = log_datetime_out['log_datetime_cleaned']
                data['early_out'] = (86400 - log_datetime_out['timedelta'].seconds) / 60 # convert timedelta seconds into minutes


            # if not log_datetime_in:
            #     ret['data'].append({
            #         'schedule_timetable_id': schedule_timetable_id,
            #         'final_date_time_in': final_date_time_in,
            #         'final_date_time_out': final_date_time_out,
            #         'is_absent': False,
            #         'late_in': late_in,
            #         'early_out': early_out,
            #         'ot_hours': 0,
            #         'ot_premium_hours': 0,
            #         'log_id_in': None,
            #         'log_id_out': log_datetime_out['log_id'],
            #     })
            # elif not log_datetime_out:
        ret['data'] = data
            # update log so that it will not be used again
            # log_in = Log.objects.get(pk=log_datetime_in['log_id'])
            # log_out = Log.objects.get(pk=log_datetime_out['log_id'])
            # log_in.is_used = True
            # log_in.save()
            # log_out.is_used = True
            # log_out.save()

    return ret['data']

def compute_dtr(employee_ids, dates):

    # get employees and loop through them
    employee_ids = employee_ids
    date_list = dates
    employees = Employee.objects.filter(id__in=employee_ids)
    for employee in employees:
        schedules = Schedule.objects.filter(date__in=date_list, employee_id=employee.id)

        for date in date_list:

            attendance = Attendance.objects.filter(employee_id=employee.id, date=date).first()
            # if no attendance record yet for the employee AND date THEN create attendance
            if not attendance:
                # attendance fields
                remarks = 'generated by PayrollOne powered by iamhanz.com'
                attendance = Attendance(employee=employee, date=date, remarks=remarks)
                attendance.save()


            schedule = schedules.filter(date=date)[0]
            schedule_timetables = schedule.scheduletimetable_set.all()
                
            attendancelogs = []

            for sched_timetable in schedule_timetables:
                final_date_time_in = timezone.now()
                final_date_time_out = timezone.now()

                # create attendancelog and add to attendance
                attendancelog = AttendanceLog(final_date_time_in=final_date_time_in, final_date_time_out=final_date_time_out, schedule_timetable=sched_timetable)
                attendancelogs.append(attendancelog)

            AttendanceLog.objects.filter(attendance_id=attendance.id).delete()
            attendance.attendancelog_set.set(attendancelogs, bulk=False)
            attendance.save()

    return 'done'