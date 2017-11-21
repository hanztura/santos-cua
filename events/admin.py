from django.contrib import admin

from events.models import Event


# class ContactAddressInline(admin.TabularInline):
#     model = Address
#     extra = 0
#     classes = ('grp-collapse grp-closed',)


class EventAdmin(admin.ModelAdmin):
    fields = ['title', 'resource_persons', 'location', 'description', 'cpd_units', 'reg_fee' ]

    list_display = ['title', 'location']

    # inlines = [ContactAddressInline, ContactPhoneInline, ContactEmailInline,]



# Register your models here.
admin.site.register(Event, EventAdmin)