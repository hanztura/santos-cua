from django.contrib import admin

from .models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Bio', {'fields': [
            'contact',
            'id_num',
            'abbr'
        ]}),
        ('Dates', {'fields': ['date_hired', 'date_resigned']}),
    ]

    list_display = ['contact', 'abbr', 'id_num', 'date_hired', 'is_resigned']
    list_filter = []
    search_fields = ['contact__first_name', 'contact__last_name', 'contact__middle_name']

# Register your models here.
admin.site.register(Employee, EmployeeAdmin)