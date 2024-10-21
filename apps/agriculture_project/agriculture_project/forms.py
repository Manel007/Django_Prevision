from django import forms
from .models import CropYield

class YieldForm(forms.ModelForm):
    class Meta:
        model = CropYield
        fields = ['area', 'item', 'year', 'hg_per_ha_yield', 'average_rain_fall', 'pesticides_tonnes', 'avg_temp']  # Corrected field name
