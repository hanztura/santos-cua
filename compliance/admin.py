from django.contrib import admin

from .models import Client, ClientPractitioner, BirCompliance, BirDeadline, DeadlineStatus


class ClientPractitionerInline(admin.TabularInline):
    model = ClientPractitioner
    extra = 0


class BirComplianceInline(admin.TabularInline):
    model = BirCompliance
    extra = 0


class ClientAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            'contact',
            'rdo',
            'line_of_business',
            'date_start',
            'date_end',
            'is_active',
        ]}),
    ]

    list_display = ['contact', 'is_active', 'rdo', 'line_of_business','is_deleted']
    list_filter = ['is_active', 'rdo', 'line_of_business']
    search_fields = ['contact__first_name', 'contact__last_name', 'contact__registered_name']
    inlines = [ClientPractitionerInline, BirComplianceInline]



class BirDeadlineAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            'compliance',
            # 'month',
            # 'day',
            # 'year',
            'date_deadline',
            'date_notify_start',
        ]}),
    ]

    list_display = ['compliance', 'date_deadline', 'date_notify_start']
    list_filter = ['date_notify_start', 'date_deadline']


class DeadlineStatusAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            'bir_deadline',
            'status',
            'as_of',
        ]}),
    ]

    list_display = ['bir_deadline', 'status', 'as_of']
    list_filter = ['status']
    search_fields = ['bir_deadline__compliance__client__contact__alias']


# Register your models here.

admin.site.register(Client, ClientAdmin)
admin.site.register(BirDeadline, BirDeadlineAdmin)
admin.site.register(DeadlineStatus, DeadlineStatusAdmin)