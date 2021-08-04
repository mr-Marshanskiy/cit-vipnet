from django.forms import fields
from events.models import Device, Distributor
from django import forms


class MoveDeviceForm(forms.ModelForm):
    old_type = forms.ModelChoiceField(
        queryset=Device.objects.all(),
        label='Удаляемое устройство'
    )
    new_type = forms.ModelChoiceField(
        queryset=Device.objects.all(),
        label='Преемник устройство'
    )
    class Meta:
        model = Device
        fields = ('old_type', 'new_type')

class MoveDistributorForm(forms.ModelForm):
    old_seller = forms.ModelChoiceField(
        queryset=Distributor.objects.all(),
        label='Удаляемый дистрибьютор'
    )
    new_seller = forms.ModelChoiceField(
        queryset=Distributor.objects.all(),
        label='Преемник дистрибьютор'
    )
    class Meta:
        model = Distributor
        fields = ('old_seller', 'new_seller')