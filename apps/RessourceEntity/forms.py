from django import forms
from .models import Ressource, Fournisseur

class RessourceForm(forms.ModelForm):
    class Meta:
        model = Ressource
        fields = ['nom_ressource','type_ressource', 'quantite', 'unite_mesure', 'zone']


class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom', 'type_fournisseur', 'adresse', 'numero_telephone', 'ressources_fournies']

class PredictForm(forms.Form):
    nom_ressource = forms.CharField(label='Nom de la ressource', max_length=100)
    saison = forms.ChoiceField(choices=[('winter', 'Winter'), ('spring', 'Spring'), 
                                        ('summer', 'Summer'), ('fall', 'Fall')])