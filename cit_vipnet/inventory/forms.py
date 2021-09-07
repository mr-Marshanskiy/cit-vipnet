from django import forms
from .models import Coordinator


class CoordinatorForm(forms.ModelForm):
    class Meta:
        model = Coordinator
        fields = '__all__'
