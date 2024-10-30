from django import forms
from apps.Culture.models import CultureAgricole

class RecommendationForm(forms.Form):
    CHOIX_CULTURE = [('existing', 'Existing Agricultural Crop'), ('custom', 'Custom Data ')]
    choix_culture = forms.ChoiceField(choices=CHOIX_CULTURE, widget=forms.RadioSelect)
    culture_existante = forms.ModelChoiceField(queryset=CultureAgricole.objects.all(), required=False, label="Culture existante")
    cycle_croissance_jours = forms.IntegerField(required=False, label="Cycle de croissance (jours)")
    type_sol_prefere = forms.CharField(max_length=100, required=False, label="Type de sol préféré")
    zone_culture_recommandee = forms.CharField(max_length=100, required=False, label="Zone climatique recommandée")

    def clean(self):
        cleaned_data = super().clean()
        choix_culture = cleaned_data.get("choix_culture")

        if choix_culture == 'existing' and not cleaned_data.get("culture_existante"):
            self.add_error("culture_existante", "Please select an existing crop.")
        elif choix_culture == 'custom' and not (cleaned_data.get("cycle_croissance_jours") and cleaned_data.get("type_sol_prefere") and cleaned_data.get("zone_culture_recommandee")):
            raise forms.ValidationError("Please fill in all fields for custom data.")
        return cleaned_data
