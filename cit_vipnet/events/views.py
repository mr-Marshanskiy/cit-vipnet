from django.shortcuts import render, get_object_or_404, redirect
from .models import Device, Distributor, License, Vpn, Organisation
from django.db.models import Q, Count, Subquery, OuterRef

from django.views.generic import ListView, DetailView

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
        'organisations.html',
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
    ).order_by('-date')

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

def single_act(request, pk):
    lic = License.objects.prefetch_related().get(id=pk)
    vpn = lic.lics.all().order_by('network', 'organisation', 'vpn_number', )
    return render(
        request,
        'single_act.html',
        {
            'vpn': vpn,
            'lic': lic,
        }
    )


class DistributorListView(ListView):
    model = Distributor
    context_object_name = 'page'
    queryset = Distributor.objects.all().annotate(
        lic_count=Count('distributors')
    ).order_by('-lic_count')
    template_name = 'distributors.html'


class DevicesListView(ListView):
    model = Device
    context_object_name = 'page'
    queryset = Device.objects.all().annotate(
        device_count=Count('devices')
    ).order_by('-device_count')
    template_name = 'devices.html'

class DistributorDetailView(DetailView):
    model = Distributor
    context_object_name = 'seller'
    template_name = 'single_distributor.html'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lics'] = License.objects.filter(distributor=self.object).order_by('-date')
        return context


class DevicesDetailView(DetailView):
    model = Device
    context_object_name = 'device'
    template_name = 'single_device.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vpn'] = Vpn.objects.filter(device_type=self.object).order_by('-reg_date')
        return context
   