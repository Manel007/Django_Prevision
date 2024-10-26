# forms.py
from django import forms
from .models import ZoneGeographique, TypeDeSol

class ZoneGeographiqueForm(forms.ModelForm):
    type_de_sol = forms.ModelChoiceField(
        queryset=TypeDeSol.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Sol Type",
        label='Geographic Zone Sol Type'
    )

    class Meta:
        model = ZoneGeographique
        fields = ['nomZone', 'latitude', 'longitude', 'annee', 'temperatureMoyenne', 'pluviometrie', 'type_de_sol', 'description']
        labels = {
            'nomZone': 'Name of the Geographic Zone',
            'description': 'Description (optional)',
            'latitude': 'Latitude (°)',
            'longitude': 'Longitude (°)',
            'annee': 'Reference Year for Meteorological Conditions',
            'temperatureMoyenne': 'Average Temperature (°C)',
            'pluviometrie': 'Total Precipitation (mm)',
            'type_de_sol':'Zone Sol Type'
        }
        widgets = {
            'nomZone': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'annee': forms.NumberInput(attrs={'class': 'form-control'}),
            'temperatureMoyenne': forms.NumberInput(attrs={'class': 'form-control'}),
            'pluviometrie': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    # Custom validation methods remain the same
