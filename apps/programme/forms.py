from django import forms
from .models import ProgrammeDeTraitement

class ProgrammeDeTraitementForm(forms.ModelForm):
    class Meta:
        model = ProgrammeDeTraitement
        fields = ['nom', 'description', 'frequence_application', 'pesticide']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Nom du programme'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description du programme'}),
            'frequence_application': forms.Select(),
            'pesticide': forms.Select(),
        } 
