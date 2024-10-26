# forms.py
from django import forms
from .models import ZoneGeographique, TypeDeSol

class ZoneGeographiqueForm(forms.ModelForm):
    type_de_sol = forms.ModelChoiceField(
        queryset=TypeDeSol.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Sol Type",
        label='Geographic Zone Soil Type'
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
            'type_de_sol':'Zone Soil Type'
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
        if annee < 1900 or annee > 2024:
            raise forms.ValidationError("Year must be between 1900 and 2024.")
        return annee
    def clean_nomZone(self):
        nomZone = self.cleaned_data.get('nomZone')
        if not nomZone:
            raise forms.ValidationError("Zone name is required.")
        if len(nomZone) >20:  
            raise forms.ValidationError("Zone name cannot exceed 20 characters.")
        return nomZone
    def clean_temperatureMoyenne(self):
        temperatureMoyenne = self.cleaned_data.get('temperatureMoyenne')
        if temperatureMoyenne < -100 or temperatureMoyenne > 100: 
            raise forms.ValidationError("Average temperature must be between -100°C and 100°C.")
        return temperatureMoyenne

    def clean_pluviometrie(self):
        pluviometrie = self.cleaned_data.get('pluviometrie')
        if pluviometrie < 0:  
            raise forms.ValidationError("Total precipitation must be 0 or more.")
        return pluviometrie


TEXTURE_CHOICES = [
    ('Grainy', 'Grainy'),
    ('Clayey', 'Clayey'),
    ('Loamy', 'Loamy'),
    ('Silty', 'Silty'),
    ('Sandy', 'Sandy'),
    ('Peaty', 'Peaty'),
    ('Chalky', 'Chalky'),
    ('Saline', 'Saline'),
]

PROONDEUR_CHOICES = [
    ('5 cm', '5 cm'),
    ('10 cm', '10 cm'),
    ('15 cm', '15 cm'),
    ('20 cm', '20 cm'),
    ('25 cm', '25 cm'),
    ('30 cm', '30 cm'),
    ('35 cm', '35 cm'),
    ('40 cm', '40 cm'),
]

CAPACITE_RETENUE_EAU_CHOICES = [
    ('Very Low', 'Very Low'),
    ('Low', 'Low'),
    ('Moderate', 'Moderate'),
    ('High', 'High'),
    ('Very High', 'Very High'),
    ('Extreme', 'Extreme'),
    ('Saturated', 'Saturated'),
    ('Variable', 'Variable'),
]

NUTRIMENTS_DISPONIBLES_CHOICES = [
    ('Nitrogen, Phosphorus', 'Nitrogen, Phosphorus'),
    ('Potassium, Calcium', 'Potassium, Calcium'),
    ('Magnesium, Sulfur', 'Magnesium, Sulfur'),
    ('Iron, Zinc', 'Iron, Zinc'),
    ('Copper, Manganese', 'Copper, Manganese'),
    ('Boron, Molybdenum', 'Boron, Molybdenum'),
    ('Calcium, Magnesium', 'Calcium, Magnesium'),
    ('Organic Matter', 'Organic Matter'),
]



#la forme mtaa entité type sol
class TypeDeSolForm(forms.ModelForm):

    class Meta:
        model = TypeDeSol
        fields = ['nomTypeSol', 'texture', 'profondeur', 'pH', 'capacite_retenue_eau', 'nutriments_disponibles']
        labels = {
           'nomTypeSol': 'Name of Soil Type',
            'texture': 'Texture',
            'profondeur': 'Depth',
            'pH': 'pH',
            'capacite_retenue_eau': 'Water Retention Capacity',
            'nutriments_disponibles': 'Available Nutrients',
        }
        widgets = {
            'nomTypeSol': forms.TextInput(attrs={'class': 'form-control'}),
            'texture': forms.Select(choices=TEXTURE_CHOICES, attrs={'class': 'form-control'}),
            'profondeur': forms.Select(choices=PROONDEUR_CHOICES, attrs={'class': 'form-control'}),
            'pH': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacite_retenue_eau': forms.Select(choices=CAPACITE_RETENUE_EAU_CHOICES, attrs={'class': 'form-control'}),
            'nutriments_disponibles': forms.Select(choices=NUTRIMENTS_DISPONIBLES_CHOICES, attrs={'class': 'form-control'}),
        }

 
    def clean_pH(self):
        pH = self.cleaned_data.get('pH')
        if pH < 0 or pH > 14: 
            raise forms.ValidationError("Le pH doit être compris entre 0 et 14.")
        return pH