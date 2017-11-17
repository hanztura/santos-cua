from django.contrib import admin

from .models import Contact, Address, Phone, Email


class ContactAddressInline(admin.TabularInline):
    model = Address
    extra = 0
    classes = ('grp-collapse grp-closed',)



class ContactPhoneInline(admin.TabularInline):
    model = Phone
    extra = 0
    classes = ('grp-collapse grp-closed',)


class ContactEmailInline(admin.TabularInline):
    model = Email
    extra = 0
    classes = ('grp-collapse grp-closed',)


class ContactAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            'entity_type',
            'alias',
            'is_client'
        ]}),
        ('Bio - Individual', {
            'classes': ('grp-collapse grp-closed',),

            'fields': [
                'first_name',
                'last_name',
                'middle_name',
                'date_of_birth'
            ],
        }),
        ('Bio - Artificial', {
            'classes': ('grp-collapse grp-closed',),

            'fields': [
                'registered_name',
                'trade_name',
            ]
        }),
        ('Government Numbers', {
            'classes': ('grp-collapse grp-closed',),

            'fields': [
                'tax_num',
                'ss_num',
                'health_num',
                'hdmf_num'
            ]
        }),
    ]

    list_display = ['name', 'tax_num', 'is_client']
    list_filter = ['entity_type']
    search_fields = [
        'first_name',
        'last_name',
        'registered_name',
        'trade_name'
    ]
    inlines = [ContactAddressInline, ContactPhoneInline, ContactEmailInline,]



# Register your models here.
admin.site.register(Contact, ContactAdmin)