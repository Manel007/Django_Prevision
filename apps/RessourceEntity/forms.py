from django import forms
from .models import Ressource

class RessourceForm(forms.ModelForm):
    class Meta:
        model = Ressource
        fields = ['type_ressource', 'quantite', 'unite_mesure', 'zone']
