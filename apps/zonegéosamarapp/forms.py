# forms.py
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
      

    # Add custom validation methods for latitude, longitude, etc.
    def clean_latitude(self):
        latitude = self.cleaned_data.get('latitude')
        if latitude < -90 or latitude > 90:
            raise forms.ValidationError("Latitude must be between -90 and 90.")
        return latitude

    def clean_longitude(self):
        longitude = self.cleaned_data.get('longitude')
        if longitude < -180 or longitude > 180:
            raise forms.ValidationError("Longitude must be between -180 and 180.")
        return longitude

    def clean_annee(self):
        annee = self.cleaned_data.get('annee')
        if annee < 1900 or annee > 2024:  # Example range
            raise forms.ValidationError("Year must be between 1900 and 2024.")
        return annee

    def clean_nomZone(self):
        nomZone = self.cleaned_data.get('nomZone')
        if not nomZone:
            raise forms.ValidationError("Zone name is required.")
        if len(nomZone) >20:  # Assuming max_length is 20
            raise forms.ValidationError("Zone name cannot exceed 20 characters.")
        return nomZone

    def clean_temperatureMoyenne(self):
        temperatureMoyenne = self.cleaned_data.get('temperatureMoyenne')
        if temperatureMoyenne < -100 or temperatureMoyenne > 100:  # Reasonable range for temperatures
            raise forms.ValidationError("Average temperature must be between -100°C and 100°C.")
        return temperatureMoyenne

    def clean_pluviometrie(self):
        pluviometrie = self.cleaned_data.get('pluviometrie')
        if pluviometrie < 0:  # Precipitation cannot be negative
            raise forms.ValidationError("Total precipitation must be 0 or more.")
        return pluviometrie
