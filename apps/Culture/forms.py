from django import forms
from .models import CultureAgricole

class CultureAgricoleForm(forms.ModelForm):
    class Meta:
        model = CultureAgricole
        fields = ['nom', 'description', 'cycle_croissance_jours', 'rendement_attendu', 'zone_culture_recommandee', 'type_sol_prefere', 'irrigation']