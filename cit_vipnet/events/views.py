from django.shortcuts import render, get_object_or_404, redirect
from .models import License, Vpn, Organisation
from django.db.models import Q, Count, Subquery, OuterRef



def index(request):
    query = request.GET.get('q')
    if not query:
        query = ''
    page = Vpn.objects.filter(
        Q(organisation__inn__icontains=query) | 
        Q(license__act__icontains=query) | 
        Q(organisation__full_name__icontains=query) |
        Q(organisation__short_name__icontains=query)
    ).select_related()
    return render(
        request,
        'index.html',
        {
            'page': page,
        }
     )

def orgs(request):
    query = request.GET.get('q')
    if not query:
        query = ''
    page = Organisation.objects.prefetch_related().filter(
        Q(inn__icontains=query) | 
        Q(full_name__icontains=query) |
        Q(short_name__icontains=query)
    ).annotate(vpn_count=Count('orgs__vpn_number', distinct=True))
    
    return render(
        request,
        'organisation.html',
        {
            'page': page,
        }
    )

def acts(request):
    query = request.GET.get('q')
    if not query:
        query = ''
    page = License.objects.prefetch_related().filter(
        Q(act__icontains=query) | 
        Q(distributor__name__icontains=query)
    )

    return render(
        request,
        'acts.html',
        {
            'page': page,
        }
    )

def single_org(request, inn):
    org = Organisation.objects.prefetch_related().get(inn=inn)
    vpn = org.orgs.all().order_by('network', 'vpn_number', '-reg_date', '-reg_number')
    return render(
        request,
        'single_org.html',
        {
            'vpn': vpn,
            'org': org,
        }
    )

def single_act(request, act):
    lic = License.objects.prefetch_related().get(id=act)
    vpn = lic.lics.all().order_by('network', 'organisation', 'vpn_number', )
    return render(
        request,
        'single_act.html',
        {
            'vpn': vpn,
            'lic': lic,
        }
    )