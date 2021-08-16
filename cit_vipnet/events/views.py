from django.urls.base import reverse_lazy
from .forms import DistributorForm, DeviceForm, VpnForm, OrganisationForm
import datetime
from django.conf import settings
from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404, redirect
from .models import Device, Distributor, License, Vpn, Organisation, Network
from django.db.models import Q, Count
from django.http import Http404
from django.views.generic.edit import DeletionMixin, FormMixin

from django.views.generic import ListView, DetailView, DeleteView, CreateView
from django.views.generic.detail import SingleObjectMixin


'''
Функция заменена IndexListView
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

Функция заменена OrganisationListView
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

# Функция заменена OrganisationSingle

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


# Функция заменена LicenseListView

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
'''

class IndexListView(ListView):
    paginate_by = 100
    model = Vpn
    template_name = 'index.html'

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q')
        if not query:
            queryset = Vpn.objects.all().select_related().order_by(
                '-reg_date', '-reg_number')
            return queryset
        queryset = Vpn.objects.filter(
            Q(organisation__inn__icontains=query) |
            Q(license__act__icontains=query) |
            Q(organisation__full_name__icontains=query) |
            Q(organisation__short_name__icontains=query)
        ).select_related().order_by('-reg_date', '-reg_number')
        return queryset


class OrganisationListView(ListView):
    paginate_by = 100
    model = Organisation
    template_name = 'organisations.html'

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q')
        if not query:
            queryset = Organisation.objects.all().annotate(vpn_count=Count(
                'orgs__vpn_number', distinct=True)).order_by('-reg_number')
            return queryset
        queryset = Organisation.objects.prefetch_related().filter(
            Q(inn__icontains=query) | Q(full_name__icontains=query) |
            Q(short_name__icontains=query)).annotate(
            vpn_count=Count('orgs__vpn_number', distinct=True)
        ).order_by('-reg_number')
        return queryset


class LicenseListView(ListView):
    paginate_by = 100
    model = License
    template_name = 'acts.html'

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q')
        if not query:
            queryset = License.objects.prefetch_related(
                ).annotate(used_count=Count('lics')).order_by('-date')
            return queryset
        queryset = License.objects.prefetch_related().filter(
            Q(act__icontains=query) |
            Q(distributor__name__icontains=query)
        ).annotate(used_count=Count('lics')).order_by('-date')
        return queryset

# Данные об организации со списком выданной СКИ
class OrganisationSingleView(SingleObjectMixin, ListView):
    paginate_by = 10
    template_name = 'single_org.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Organisation.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = self.object
        context['vpn'] = self.objects
        return context

    def get_queryset(self):
        self.objects = self.object.orgs.all().order_by('network', 'vpn_number', '-reg_date', '-reg_number')
        return self.objects



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
    queryset = Distributor.objects.prefetch_related().annotate(
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
            queryset = Distributor.objects.prefetch_related().annotate(
                lic_count=Count('distributors')
            ).order_by('-lic_count')
            success_url = reverse_lazy('sellers')
            return queryset
        queryset = Distributor.objects.prefetch_related().filter(
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


class DistributorDetailView(DetailView):
    model = Distributor
    context_object_name = 'seller'
    template_name = 'single_distributor.html'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lics'] = License.objects.filter(distributor=self.object).order_by('-date')
        return context


class DevicesListView(FormListView):
    form_class = DeviceForm
    model = Device
    context_object_name = 'page'
    queryset = Device.objects.all().annotate(
        device_count=Count('devices')
    ).order_by('-device_count')
    success_url = reverse_lazy('devices')
    template_name = 'devices.html'


class DeviceListForDeleteView(ListView):
    model = Device
    context_object_name = 'page'
    template_name = 'delete_devices.html'

    def get_queryset(self, *args, **kwargs):
        success_url = reverse_lazy('devices')
        query = self.request.GET.get('q')
        if not query:
            queryset = Device.objects.all().annotate(
                device_count=Count('devices')
            ).order_by('-device_count')
            return queryset
        queryset = Device.objects.filter(
            type__icontains=query).annotate(
            device_count=Count('devices')
        ).order_by('-device_count')
        return queryset


class DevicesDeleteView(DeleteView):
    model = Device
    success_url = reverse_lazy('deleting_list_devices')

    def get(self, *a, **kw):
        return self.delete(*a, **kw)


class DevicesDetailView(DetailView):
    model = Device
    context_object_name = 'device'
    template_name = 'single_device.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vpn'] = Vpn.objects.filter(device_type=self.object).order_by('-reg_date')
        return context


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


class LicenseSingleView(SingleObjectMixin, ListView):
    template_name = 'single_act.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=License.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lic'] = self.object
        context['vpn'] = self.objects
        return context

    def get_queryset(self):
        self.objects = self.object.lics.all().order_by('network', 'vpn_number', '-reg_date', '-reg_number')
        return self.objects


class CreateOrgView(CreateView):
    form_class = OrganisationForm
    template_name = 'new/new_org.html'
    success_url = reverse_lazy('orgs')


class CreateVpnView(CreateView):
    form_class = VpnForm
    template_name = 'new/new_vpn.html'
    success_url = reverse_lazy('index')

    today = datetime.date.today()
    last_reg_n = Vpn.objects.first()
    try:
        last_reg_n.reg_number = str(int(last_reg_n.reg_number) + 1)
    except:
        pass
    try:
        network = Network.objects.get(number='1760')
    except:
        network = Network.objects.first()
    try:
        device = Device.objects.get(type='USB')
    except:
        device = Device.objects.first()
    initial = {
        'reg_number': last_reg_n.reg_number,
        'reg_date': today,
        'network': network,
        'device_type': device,
        'license_date': today,
        'license_amount': 1,
        'vpn_number': 0,
    }

    def get_initial(self):
        init = super(CreateVpnView, self).get_initial()
        try:
            vpn_number = Vpn.objects.filter(organisation__pk=self.kwargs.get(
                'pk')).order_by('-vpn_number').first().vpn_number
            vpn_number += 1
        except:
            vpn_number = 0
        self.initial['vpn_number'] = vpn_number
        return init


    def form_valid(self, form):
        form.instance.organisation = Organisation.objects.get(
            pk=self.kwargs.get('pk'))
        lic_act = form.data.get('license_act')
        lic_date = form.data.get('license_date')
        lic_distr = form.data.get('license_ distributor')
        lic_amount = form.data.get('license_amount')
        date_clean = datetime.datetime.strptime(lic_date, '%d.%m.%Y')
        lic, created = License.objects.get_or_create(
            act=lic_act, date=date_clean, distributor=lic_distr, amount=lic_amount)
        form.instance.license = lic
        return super(CreateVpnView, self).form_valid(form)


class SingleLicenseDeleteView(DeleteView):
    model = License
    success_url = reverse_lazy('index')
    template_name = 'confirm_deleting.html'


class OrgListVpnDeleteView(DeleteView):
    model = Vpn
    template_name = 'confirm_deleting.html'

    def get_success_url(self):
        org_id = self.object.organisation.id
        return reverse_lazy('single_org', kwargs={'pk': org_id})


class OrganisationDeleteView(DeleteView):
    model = Organisation
    success_url = reverse_lazy('index')
    template_name = 'confirm_deleting.html'