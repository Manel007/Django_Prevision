from django import forms
from .models import ZoneGeographique

class ZoneGeographiqueForm(forms.ModelForm):
    class Meta:
        model = ZoneGeographique
        fields = ['nomZone', 'latitude', 'longitude', 'annee', 'temperatureMoyenne', 'pluviometrie', 'description']
        labels = {
            'nomZone': 'Name of the Geographic Zone',
            'description': 'Description (optional)',
            'latitude': 'Latitude (°)',
            'longitude': 'Longitude (°)',
            'annee': 'Reference Year for Meteorological Conditions',
            'temperatureMoyenne': 'Average Temperature (°C)',
            'pluviometrie': 'Total Precipitation (mm)',
        }
