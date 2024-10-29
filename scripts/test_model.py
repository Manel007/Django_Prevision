import joblib
import pandas as pd

# Charger le modèle KNN sauvegardé
model = joblib.load('trained_model.pkl')

# Créer un DataFrame avec des exemples de données à tester
# Remplacez les noms de colonnes par ceux utilisés lors de l'entraînement
data_test = pd.DataFrame({
    'cycle_croissance_jours': [30, 60],  # Exemple de cycle de croissance
    'rendement_attendu': [1000, 2000]    # Exemple de rendement
    # N'incluez pas 'impact_rendement' si ce n'était pas une caractéristique utilisée lors de l'entraînement
})

# Faire des prédictions
try:
    predictions = model.predict(data_test)
    print("Recommendation :", predictions)
except ValueError as e:
    print(f"Erreur de recommendation : {e}")
