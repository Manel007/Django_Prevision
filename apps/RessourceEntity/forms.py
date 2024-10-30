from django import forms
from .models import Ressource, Fournisseur

class RessourceForm(forms.ModelForm):
    class Meta:
        model = Ressource
        fields = ['nom_ressource', 'type_ressource', 'quantite', 'unite_mesure', 'zone']









class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom', 'type_fournisseur', 'adresse', 'numero_telephone']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Name of the supplier'}),
            'adresse': forms.TextInput(attrs={'placeholder': 'Adresse'}),
            'numero_telephone': forms.TextInput(attrs={'placeholder': 'Numéro de téléphone'}),
        }
        labels = {
            'nom': 'Name of the supplier',
            'type_fournisseur': 'Type de fournisseur',
            'adresse': 'Adresse',
            'numero_telephone': 'Numéro de téléphone',
        }
class PredictForm(forms.Form):
    nom_ressource = forms.CharField(label='Nom de la Ressource', max_length=100)
    Saison = forms.ChoiceField(
        label='Saison',
        choices=[
            ('spring', 'Printemps'),
            ('summer', 'Été'),
            ('fall', 'Automne'),  # Modifié ici
            ('winter', 'Hiver'),
        ]
    )
