from django import forms
from .models import Pesticide

class PesticideForm(forms.ModelForm):
    class Meta:
        model = Pesticide
        fields = ['domain','area','element','item', 'year', 'unit']  
