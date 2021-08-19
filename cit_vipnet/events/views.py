from django.urls.base import reverse_lazy
from .forms import DistributorForm, DeviceForm, VpnForm, OrganisationForm
import datetime

from django.shortcuts import render, get_object_or_404, redirect
from .models import Device, Distributor, License, Vpn, Organisation, Network
from django.db.models import Q, Count

from django.views.generic.edit import FormMixin

from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.views.generic.detail import SingleObjectMixin


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


class IndexListView(ListView):
    paginate_by = 100
    model = Vpn
    template_name = 'index.html'

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q')
        filter
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


class OrgListVpnDeleteView(DeleteView):
    model = Vpn
    template_name = 'confirm_deleting.html'

    def get_success_url(self):
        org_id = self.object.organisation.id
        return reverse_lazy('single_org', kwargs={'pk': org_id})


class OrganisationDeleteView(DeleteView):
    model = Organisation
    success_url = reverse_lazy('orgs')
    template_name = 'confirm_deleting.html'


class OrganisationCreateView(CreateView):
    form_class = OrganisationForm
    template_name = 'new/new_org.html'

    today = datetime.date.today()
    last_reg_n = Organisation.objects.first()
    try:
        last_reg_n.reg_number = str(int(last_reg_n.reg_number) + 1)
    except:
        pass
    initial = {
        'reg_number': last_reg_n.reg_number,
        'reg_date': today,
    }

    def get_success_url(self):
        return reverse_lazy('single_org', kwargs={'pk': self.object.pk})


class OrganisationUpdateView(UpdateView):

    model = Organisation
    form_class = OrganisationForm
    template_name = 'new/new_org.html'

    def get_success_url(self):
        return reverse_lazy('single_org', kwargs={'pk': self.object.pk})


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


class LicenseSingleDeleteView(DeleteView):
    model = License
    success_url = reverse_lazy('index')
    template_name = 'confirm_deleting.html'


class VpnCreateView(CreateView):
    form_class = VpnForm
    template_name = 'new/new_vpn.html'

    def get_initial(self):
        today = datetime.date.today()
        last_reg_n = Vpn.objects.all().order_by('-reg_date', '-reg_number').first()
        try:
            last_reg_n.reg_number = str(int(last_reg_n.reg_number) + 1)
            print((last_reg_n.reg_number))
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
        try:
            vpn_number = Vpn.objects.filter(organisation__pk=self.kwargs.get(
                'pk')).order_by('-vpn_number').first().vpn_number
            vpn_number += 1
        except:
            vpn_number = 0

        self.initial = {
            'reg_number': last_reg_n.reg_number,
            'reg_date': today,
            'network': network,
            'device_type': device,
            'license_date': today,
            'license_amount': 1,
            'vpn_number': vpn_number,
        }

        init = super(VpnCreateView, self).get_initial()
        return init

    def get_success_url(self):
        org_id = self.object.organisation.id
        return reverse_lazy('single_org', kwargs={'pk': org_id})

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
        return super(VpnCreateView, self).form_valid(form)


class VpnUpdateView(UpdateView):

    model = Vpn
    form_class = VpnForm
    template_name = 'new/new_vpn.html'

    def form_valid(self, form):
        lic_act = form.data.get('license_act')
        lic_date = form.data.get('license_date')
        lic_distr = form.data.get('license_ distributor')
        lic_amount = form.data.get('license_amount')
        date_clean = datetime.datetime.strptime(lic_date, '%d.%m.%Y')
        lic, created = License.objects.get_or_create(
            act=lic_act, date=date_clean, distributor=lic_distr, amount=lic_amount)
        form.instance.license = lic
        return super(VpnUpdateView, self).form_valid(form)

    def get_success_url(self):
        org_id = self.object.organisation.id
        return reverse_lazy('single_org', kwargs={'pk': org_id})

    def get_initial(self):

        self.initial = {}
        try:
            self.initial['license_act'] = self.object.license.act
        except:
            self.initial['license_act'] = ''
        try:
            self.initial['license_date'] = self.object.license.date
        except:
            today = datetime.date.today()
            self.initial['license_date'] = today
        try:
            self.initial['license_amount'] = self.object.license.amount
        except:
            self.initial['license_amount'] = 1
        try:
            self.initial['license_distributor'] = self.object.license.distributor
        except:
            self.initial['license_distributor'] = ''


        init = super(VpnUpdateView, self).get_initial()
        return init