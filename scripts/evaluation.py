import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import joblib

model = joblib.load('trained_model.pkl')

merged_df = pd.read_csv('merged_data.csv')

X = merged_df[['cycle_croissance_jours', 'rendement_attendu', 'zone_culture_recommandee','impact_rendement',]]
y = merged_df['culture']

# Prédiction
y_pred = model.predict(X)

# Évaluation
print("Matrice de confusion :\n", confusion_matrix(y, y_pred))
print("\nRapport de classification :\n", classification_report(y, y_pred))
