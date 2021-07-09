from django.db.models.fields import related
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, License, Organisation, Reglament
from django.db.models import Count, F, Sum

def index(request):

    page = Event.objects.select_related(
        'organisation'
    ).prefetch_related()[:50]
    return render(
        request,
        'index.html',
        {
            'page': page,
        }
     )


def org_single(request, inn):
    org = get_object_or_404(Organisation.objects.prefetch_related(), org_inn=inn)
    
    sorted_event = sorted(org.reg_numbers.all(), key=lambda x: (x.keys_date), reverse=True)
    new_list = {}
    for vpn in sorted_event:
        new_list.setdefault(vpn.vpn_number, []).append(vpn)
    
    return render(
        request,
        'organisation_single.html',
        {
            'org': org,
            'events': new_list,
        }
    )


def events(request):
    
    page = Event.objects.all().select_related()
    
    page1 = Reglament.objects.all().select_related()

    print(page.query)
    print(page1.query)
    return render(
        request,
        'events.html',
        {
            'page': page,
        }
     )


def licenses(request):
    page = License.objects.all().prefetch_related().annotate(
        dcount=Count('license')
    )
    page = sorted(page, key=lambda x: (x.ammount), reverse=True)

    return render(
        request,
        'licenses.html',
        {
            'page': page,
        }
    )