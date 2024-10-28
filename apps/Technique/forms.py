from django import forms
from .models import TechniqueCulture

class TechniqueCultureForm(forms.ModelForm):
    class Meta:
        model = TechniqueCulture
        fields = ['nom_technique', 'description', 'impact_rendement', 'cultures_associees']