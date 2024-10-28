from django import forms

class RecommendationForm(forms.Form):
    type_sol_prefere = forms.CharField(max_length=100)
    cycle_croissance_jours = forms.IntegerField()
    zone_culture_recommandee = forms.CharField(max_length=100)
    rendement_attendu = forms.FloatField(required=False)  # Champ optionnel
