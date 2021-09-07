from django.urls.base import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.db.models import Q

from .forms import CoordinatorForm
from .models import Coordinator


class CoordListView(ListView):
    model = Coordinator
    context_object_name = 'page'
    template_name = 'coords.html'

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q')
        filter
        if not query:
            queryset = Coordinator.objects.all().select_related().order_by(
                '-date')
            return queryset
        queryset = Coordinator.objects.filter(
            Q(network__number__icontains=query) |  #номер сети
            Q(address__icontains=query) |  #Местоположение
            Q(name__icontains=query) |  #Название узла
            Q(vipnet_id__icontains=query) |  #ID в сети
            Q(modification__name__icontains=query) |  # Модификация
            Q(hardware_platform__name__icontains=query) |  # Аппаратная платформа
            Q(serial_number__icontains=query) |  # Серийный номер
            Q(account_number_skzi__icontains=query) |  # У/Н СКЗИ
            Q(account_number_fstec__icontains=query)  # У/Н ФСТЭК
        ).select_related().order_by('-date')
        return queryset


class CoordCreateView(CreateView):
    form_class = CoordinatorForm
    template_name = 'new/coord.html'


class CoordUpdateView(UpdateView):
    model = Coordinator
    form_class = CoordinatorForm
    template_name = 'new/coord.html'


class CoordDetailView(DetailView):
    model = Coordinator
    context_object_name = 'coord'
    template_name = 'single_coord.html'


class CoordDeleteView(DeleteView):
    model = Coordinator
    success_url = reverse_lazy('coords')
    template_name = 'confirm_deleting.html'