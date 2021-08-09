from django import forms
from django import forms

from .models import Distributor, Device

class DistributorForm(forms.ModelForm):
    class Meta:
        model = Distributor
        fields = '__all__'


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = '__all__'