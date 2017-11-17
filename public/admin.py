# from django.contrib import admin

# from contacts.models import Contact, Address, Phone
# from employees.models import Employee


# class ContactAddressInline(admin.StackedInline):
#     model = Address
#     extra = 0


# class ContactPhoneInline(admin.StackedInline):
#     model = Phone
#     extra = 0


# class ContactAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None, {'fields': [
#             'entity_type',
#             'alias',
#             'is_client'
#         ]}),
#         ('Bio - Individual', {'fields': [
#             'first_name',
#             'last_name',
#             'middle_name',
#             'date_of_birth'
#         ]}),
#         ('Bio - Artificial', {'fields': [
#             'registered_name',
#             'trade_name',
#         ]}),
#         ('Government Numbers', {'fields': [
#             'tax_num',
#             'ss_num',
#             'health_num',
#             'hdmf_num'
#         ]}),
#     ]

#     list_display = ['name', 'tax_num', 'is_client']
#     list_filter = ['entity_type']
#     search_fields = [
#         'first_name',
#         'last_name',
#         'registered_name',
#         'trade_name'
#     ]
#     inlines = [ContactAddressInline, ContactPhoneInline, ]

# class EmployeeAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('Bio', {'fields': [
#             'contact',
#             'id_num',
#             'abbr'
#         ]}),
#         ('Dates', {'fields': ['date_hired', 'date_resigned']}),
#     ]

#     list_display = ['contact', 'abbr', 'id_num', 'date_hired', 'is_resigned']
#     list_filter = []
#     search_fields = ['contact__first_name', 'contact__last_name', 'contact__middle_name']

# # Register your models here.
# admin.site.register(Contact, ContactAdmin)
# admin.site.register(Employee, EmployeeAdmin)
