from django.urls.base import reverse_lazy
from .forms import DistributorForm, DeviceForm
from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404, redirect
from .models import Device, Distributor, License, Vpn, Organisation
from django.db.models import Q, Count
from django.http import Http404
from django.views.generic.edit import DeletionMixin, FormMixin

from django.views.generic import ListView, DetailView, DeleteView

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


class FormListView(FormMixin, ListView):
    def post(self, request, *args, **kwargs):
        """ Обработка POST при использовани FormMixin в DetailView """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class DistributorListView(FormListView):
    template_name = 'distributors.html'
    form_class = DistributorForm
    model = Distributor
    context_object_name = 'page'
    queryset = Distributor.objects.all().annotate(
        lic_count=Count('distributors')
    ).order_by('-lic_count')
    success_url = reverse_lazy('sellers')


class DistributorListForDeleteView(ListView):
    model = Distributor
    context_object_name = 'page'
    template_name = 'delete_distributors.html'

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q')
        if not query:
            queryset = Distributor.objects.all().annotate(
                lic_count=Count('distributors')
            ).order_by('-lic_count')
            success_url = reverse_lazy('sellers')
            return queryset
        queryset = Distributor.objects.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query)
        ).annotate(
            lic_count=Count('distributors')
        ).order_by('-lic_count')
        return queryset


class DistributorDeleteView(DeleteView):
    model = Distributor
    success_url = reverse_lazy('deleting_list_sellers')

    def get(self, *a, **kw):
        return self.delete(*a, **kw)


class DevicesListView(FormListView):
    form_class = DeviceForm
    model = Device
    context_object_name = 'page'
    queryset = Device.objects.all().annotate(
        device_count=Count('devices')
    ).order_by('-device_count')
    success_url = reverse_lazy('devices')
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
