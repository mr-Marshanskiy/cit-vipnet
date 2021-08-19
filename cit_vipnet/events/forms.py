from django.conf import settings
from django import forms
from .models import Distributor, Device, Vpn, Organisation, License
from django.utils.translation import ugettext_lazy as _

class DistributorForm(forms.ModelForm):
    class Meta:
        model = Distributor
        fields = '__all__'


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = '__all__'


class LicenseForm(forms.ModelForm):
    class Meta:
        model = License
        fields = '__all__'
class OrganisationForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = '__all__'


class VpnForm(forms.ModelForm):
    license_act = forms.CharField(max_length=30)
    license_date = forms.DateField()
    license_amount = forms.IntegerField()
    license_distributor = forms.ModelChoiceField(
        queryset=Distributor.objects.all())

    class Meta:
        model = Vpn
        fields = ['network', 'reg_number', 'reg_date', 'vpn_number',
                  'device_type', 'device_id', 'license_act', 'license_date',
                  'license_amount', 'license_distributor', 'comment']
        labels = {
            'license_act': _('Номер акта'),
            'license_date': _('Дата акта'),
            'license_amount': _('Кол-во лицензий'),
            'license_distributor': _('Дистрибьютор'),
        }

    def __init__(self, *args, **kwargs):
        super(VpnForm, self).__init__(*args, **kwargs)
        self.fields['license_act'].label = _('Номер акта')
        self.fields['license_date'].label = _('Дата акта')
        self.fields['license_amount'].label = _('Кол-во лицензий')
        self.fields['license_distributor'].label = _('Дистрибьютор')
        self.fields['network'].label = _('Защищенная сеть')

