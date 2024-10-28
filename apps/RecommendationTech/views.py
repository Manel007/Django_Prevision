from django.shortcuts import render
import joblib
import pandas as pd
from .RecommendationForm import RecommendationForm  # Assurez-vous que l'importation est correcte
from apps.Culture.models import CultureAgricole

def recommend_technique(type_sol, periode_croissance, zone_culture):
    model = joblib.load('trained_model.pkl')  # Chargez votre modèle
    new_data = pd.DataFrame({
        'cycle_croissance_jours': [periode_croissance],
        'zone_culture_recommandee': [zone_culture],
        'type_sol_prefere': [type_sol]
    })
    print("Colonnes dans new_data :", new_data.columns.tolist())  # Vérifiez les colonnes ici
    predicted_technique = model.predict(new_data)
    return predicted_technique[0]

def recommend_view(request):
    recommendation = None  # Pour stocker la recommandation
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            type_sol = form.cleaned_data['type_sol_prefere']
            periode_croissance = form.cleaned_data['cycle_croissance_jours']
            zone_culture = form.cleaned_data['zone_culture_recommandee']
        
            
            # Appel à la fonction de recommandation
            recommendation = recommend_technique(type_sol, periode_croissance, zone_culture)
    else:
        form = RecommendationForm()

    return render(request, 'RecommendationTech/recommend.html', {'form': form, 'recommendation': recommendation})

