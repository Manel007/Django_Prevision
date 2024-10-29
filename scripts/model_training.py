import sys
import os
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier

sys.path.append('C:\\Users\\oumai\\Desktop\\Django_Prevision')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()  # Initialise Django

# Chargement des données
df_culture = pd.read_csv("cultures_cleaned.csv")
df_technique = pd.read_csv("techniques_cleaned.csv")
df_association = pd.read_csv("association_culture_technique.csv")


# Vérification des colonnes utilisées pour l'entraînement
print("Colonnes utilisées pour l'entraînement :", df_culture.columns.tolist())

# Vérification que les données sont chargées correctement
print(f"Dimensions de df_culture: {df_culture.shape}")
print(f"Dimensions de df_technique: {df_technique.shape}")
print(f"Dimensions de df_association: {df_association.shape}")

# Distribution des techniques
print("Distribution des techniques dans df_association:")
print(df_association['technique'].value_counts())

# Préparer les données
df_combined = df_culture.merge(df_association, left_on='nom', right_on='culture', how='inner')

# Extraire les caractéristiques (X) et la cible (y) de df_combined
X = df_combined[['cycle_croissance_jours', 'zone_culture_recommandee', 'type_sol_prefere']]
y = df_combined['technique']  # Utilisez 'technique' comme cible

# Convertir les colonnes catégorielles en chaînes de caractères
X['zone_culture_recommandee'] = X['zone_culture_recommandee'].astype(str)
X['type_sol_prefere'] = X['type_sol_prefere'].astype(str)

# Vérification de la dimension de X et y après ajustement
print(f"Dimensions de X: {X.shape}")
print(f"Dimensions de y: {y.shape}")
# Transformation des colonnes catégorielles et normalisation des données
numeric_features = ['cycle_croissance_jours']
categorical_features = ['zone_culture_recommandee', 'type_sol_prefere']

# Création d'un préprocesseur
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(), categorical_features)
    ]
)

# Entraînement du modèle avec validation croisée pour différents valeurs de K
k_values = [3, 5, 7, 9]  # Liste des valeurs de K à tester
best_k = None
best_score = 0

# Création d'un pipeline
model_pipeline = Pipeline(steps=[('preprocessor', preprocessor), 
                                  ('classifier', KNeighborsClassifier())])

for k in k_values:
    model_pipeline.set_params(classifier__n_neighbors=k)
    scores = cross_val_score(model_pipeline, X, y, cv=5)  # Validation croisée avec 5 plis
    mean_score = scores.mean()
    print(f"Score moyen pour K={k}: {mean_score}")

    if mean_score > best_score:
        best_score = mean_score
        best_k = k

print(f"Meilleure valeur pour K: {best_k} avec un score moyen de {best_score}")

# Entraînement du modèle final avec la meilleure valeur de K
model_pipeline.set_params(classifier__n_neighbors=best_k)
model_pipeline.fit(X, y)

# Sauvegarde du modèle pour l'utiliser dans des prédictions futures
joblib.dump(model_pipeline, 'trained_model.pkl')

print("Modèle entraîné et sauvegardé dans 'trained_model.pkl'.")
