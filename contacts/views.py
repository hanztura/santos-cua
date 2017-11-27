from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.forms import model_to_dict
from django.db.models import Q

# pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Contact
from .forms import ContactForm, PhoneFormSet, AddressFormSet, EmailFormSet


def index(request):
    q = request.GET.get('q')
    page = request.GET.get('page')

    if not q:
        q = ''
        contact_list = Contact.objects.order_by('alias')
    else:
        _q = q.lower()
        if _q == ':clients'or _q == ':c':
            contact_list = Contact.objects.filter(is_client=True).order_by('alias')
        elif _q == ':employee' or _q == ':e':
            contact_list = Contact.objects.filter(is_employee=True).order_by('alias')        
        else:
            contact_list = Contact.objects.filter(Q(alias__contains=q) | Q(tax_num__contains=q)).order_by('alias')[:10]

    paginator = Paginator(contact_list, 10)
    

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
        'page': page,
        'q': q,
        'index_url': 'contacts:index',
        'search_placeholder': 'type contact alias/tin'
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
    # formset_phone = PhoneFormSet()
    # formset_address = AddressFormSet()
    # formset_email = EmailFormSet()
        
    context = {
        'form' : form,
        # 'formset_phone': formset_phone,
        # 'formset_address': formset_address,
        # 'formset_email': formset_email
    }

    return render(request, 'contacts/new.html', context)

def create(request):
    if request.method == "POST":
        # validate form
        form = ContactForm(request.POST, request.FILES)
        # formset_phone = PhoneFormSet(request.POST)
        # formset_address = AddressFormSet(request.POST)
        # formset_email = EmailFormSet(request.POST)
        new_contact = None
        
        context = {
            'form' : form,
            # 'formset_phone': formset_phone,
            # 'formset_address': formset_address,
            # 'formset_email': formset_email
        }

        fail = render(request, 'contacts/new.html', context)

        if form.is_valid():
            new_contact = form.save()
            # formset_phone.instance = new_contact
            # formset_address.instance = new_contact
            # formset_email.instance = new_contact
        
        
        # if formset_phone.is_valid():
        #     formset_phone.save()
        # else:
        #     return fail

        # if formset_address.is_valid():
        #     formset_address.save()
        # else:
        #     return fail
            
        # if formset_email.is_valid():
        #     formset_email.save()
        # else:
        #     return fail

        return HttpResponseRedirect(reverse('contacts:detail', kwargs={'contact_id':new_contact.id}))

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
        # contact.is_deleted = True

        # contact.save()

        contact.delete()
        
    return render(request, 'alerts/deleted.html')