from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.forms import model_to_dict

# pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Contact
from .forms import ContactForm, PhoneFormSet, AddressFormSet, EmailFormSet


def index(request):
    contact_list = Contact.objects.order_by('alias')
    paginator = Paginator(contact_list, 10)

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    context = {
        'contact_list': contacts,
    }

    return render(request, 'contacts/index_cards.html', context)

def detail(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)

    # if contact.entity_type == 1:
    #     form = ContactForm(
    #         instance=contact,
    #         initial=model_to_dict(contact),
    #         exclude = ['is_deleted', 'registered_name', 'trade_name']
    #     )
    # elif contact.entity_type == 2:
    #     form = ContactForm(
    #         instance=contact,
    #         initial=model_to_dict(contact),
    #         exclude = ['is_deleted', 'first_name', 'last_name', 'middle_name']
    #     )
    # else:
    form = ContactForm(
        instance=contact,
        initial=model_to_dict(contact),
    )

    formset_phone = PhoneFormSet(instance=contact)
    formset_address = AddressFormSet(instance=contact)
    formset_email = EmailFormSet(instance=contact)


    context = {
        'form' : form,
        'contact': contact,
        'str_contact_id': str(contact.id),
        'formset_phone': formset_phone,
        'formset_address': formset_address,
        'formset_email': formset_email
    }
    return render(
        request,
        'contacts/detail.html',
        context
    )

def new(request):
    form = ContactForm()
    formset_phone = PhoneFormSet()
    formset_address = AddressFormSet()
    formset_email = EmailFormSet()
        
    context = {
        'form' : form,
        'formset_phone': formset_phone,
        'formset_address': formset_address,
        'formset_email': formset_email
    }

    return render(request, 'contacts/new.html', context)

def create(request):
    if request.method == "POST":
        # validate form
        form = ContactForm(request.POST, request.FILES)
        formset_phone = PhoneFormSet(request.POST)
        formset_address = AddressFormSet(request.POST)
        formset_email = EmailFormSet(request.POST)
        new_contact = None
        
        context = {
            'form' : form,
            'formset_phone': formset_phone,
            'formset_address': formset_address,
            'formset_email': formset_email
        }

        fail = render(request, 'contacts/new.html', context)

        if form.is_valid():
            # registered_name = form.cleaned_data['registered_name']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # middle_name = form.cleaned_data['middle_name']
            # trade_name = form.cleaned_data['trade_name']
            # entity_type = form.cleaned_data['entity_type']
            # alias = form.cleaned_data['alias']
            # tax_num = form.cleaned_data['tax_num']
            # ss_num = form.cleaned_data['ss_num']
            # health_num = form.cleaned_data['health_num']
            # hdmf_num = form.cleaned_data['hdmf_num']

            # date_of_birth = form.cleaned_data['date_of_birth']
            # # '-'.join([
            # #     form.cleaned_data['date_of_birth_year'], 
            # #     form.cleaned_data['date_of_birth_month'],
            # #     form.cleaned_data['date_of_birth_day']
            # # ])

            # is_client = form.cleaned_data['is_client']

            # contact = Contact(entity_type=entity_type, alias=alias, date_of_birth=date_of_birth)
            # contact.save()
            new_contact = form.save()
            formset_phone.instance = new_contact
            formset_address.instance = new_contact
            formset_email.instance = new_contact
            # return HttpResponseRedirect(reverse('contacts:detail', args=(contact.id,)))

        
        if formset_phone.is_valid():
            formset_phone.save()
        else:
            return fail

        if formset_address.is_valid():
            formset_address.save()
        else:
            return fail
            
        if formset_email.is_valid():
            formset_email.save()
        else:
            return fail

        return HttpResponseRedirect(reverse('contacts:index'))

def update(request, contact_id):
    if request.method == 'POST':
        contact = get_object_or_404(Contact, pk=contact_id)
        form = ContactForm(request.POST, request.FILES, instance=contact)
        formset_phone = PhoneFormSet(request.POST, instance=contact)
        formset_address = AddressFormSet(request.POST, instance=contact)
        formset_email = EmailFormSet(request.POST, instance=contact)
        
        context = {
            'form' : form,
            'contact': contact,
            'formset_phone': formset_phone,
            'formset_address': formset_address,
            'formset_email': formset_email
        }

        fail = render(request, 'contacts/detail.html', context)

        if form.has_changed():
            if form.is_valid():
                form.save()
            else:    
                return fail

        if formset_phone.has_changed():
            if formset_phone.is_valid():
                formset_phone.save()
            else:
                return fail

        if formset_address.has_changed():
            if formset_address.is_valid():
                formset_address.save()
            else:
                return fail

        if formset_email.has_changed():
            if formset_email.is_valid():
                formset_email.save()
            else:
                return fail

        return HttpResponseRedirect(reverse('contacts:index'))

def destroy(request, contact_id):
    if request.method == "POST":
        contact = Contact.objects.get(id=contact_id)
        contact.is_deleted = True

        contact.save()
        
    return HttpResponseRedirect(reverse('contacts:index'))