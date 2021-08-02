from django.shortcuts import render, get_object_or_404, redirect
from .models import Vpn, Organisation
from django.db.models import Q



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
    page = Organisation.objects.filter(
        Q(inn__icontains=query) | 
        Q(full_name__icontains=query) |
        Q(short_name__icontains=query)
    )
    return render(
        request,
        'organisation.html',
        {
            'page': page,
        }
    )

def single_org(request, inn):
    org = Organisation.objects.prefetch_related().get(inn=inn)
    vpn = org.orgs.all().order_by('vpn_number')
    return render(
        request,
        'single_org.html',
        {
            'vpn': vpn,
            'org': org,
        }
    )