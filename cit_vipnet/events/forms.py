from django import forms
from django import forms

from .models import Distributor

class DistributorForm(forms.ModelForm):
    class Meta:
        model = Distributor
        fields = '__all__'