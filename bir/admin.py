from django.contrib import admin

from .models import Rdo, BirForm, BirFormSchedule


class RdoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['code', 'rdo']}),
    ]

    list_display = ['code', 'rdo']
    search_fields = ['code', 'rdo']

class BirFormScheduleInline(admin.TabularInline):
    """docstring for BirFormScheduleInline"""
    model = BirFormSchedule
    extra = 1
        

class BirFormAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Form', {'fields': [
            'form_code',
            'form',
            'description',
        ]}),

        ('Deadline', {'fields': [
            'deadline_period',
            'deadline_cy_ref',
            'deadline_date_type',
        ]}),
    ]

    list_display = ['form_code', 'form']
    search_fields = ['form_code', 'form']
    inlines = [BirFormScheduleInline]

# Register your models here.
admin.site.register(Rdo, RdoAdmin)
admin.site.register(BirForm, BirFormAdmin)