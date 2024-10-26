from django import forms
from .models import ZoneGeographique

class ZoneGeographiqueForm(forms.ModelForm):
    class Meta:
        model = ZoneGeographique
        fields = ['nomZone', 'description', 'latitude', 'longitude', 'annee', 'temperatureMoyenne', 'pluviometrie']
        labels = {
            'nomZone': 'Nom de la Zone géographique',
            'description': 'Description (optionnelle)',
            'latitude': 'Latitude (°)',
            'longitude': 'Longitude (°)',
            'annee': 'Année de référence des conditions météorologiques',
            'temperatureMoyenne': 'Température Moyenne (°C)',
            'pluviometrie': 'Pluviométrie Totale (mm)',
        }
