from django.shortcuts import render
import joblib
import pandas as pd
from .RecommendationForm import RecommendationForm
from apps.Culture.models import CultureAgricole
##
def recommend_technique(type_sol, periode_croissance, zone_culture):
    model = joblib.load('trained_model.pkl')
    new_data = pd.DataFrame({
        'cycle_croissance_jours': [periode_croissance],
        'zone_culture_recommandee': [zone_culture],
        'type_sol_prefere': [type_sol]
    })
    predicted_technique = model.predict(new_data)
    return predicted_technique[0]

def recommend_view(request):
    recommendation = None
    technique_details = None  

    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            choix_culture = form.cleaned_data['choix_culture']
            
            if choix_culture == 'existing':
                culture = form.cleaned_data['culture_existante']
                
                type_sol = culture.type_sol_prefere
                periode_croissance = culture.cycle_croissance_jours
                zone_culture = culture.zone_culture_recommandee
            else:
                type_sol = form.cleaned_data['type_sol_prefere']
                periode_croissance = form.cleaned_data['cycle_croissance_jours']
                zone_culture = form.cleaned_data['zone_culture_recommandee']
            
            recommendation = recommend_technique(type_sol, periode_croissance, zone_culture)
            technique_details = {
                "nom_technique": recommendation,
                "description": "Description de la technique recommandée.",
                "impact_rendement": "10%",
                "date_application": "printemps"
            }
    else:
        form = RecommendationForm()

    return render(request, 'RecommendationTech/recommend.html', {
        'form': form,
        'recommendation': recommendation,
        'technique_details': technique_details
    })
