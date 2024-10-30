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
django.setup()  


df_culture = pd.read_csv("cultures_cleaned.csv")
df_technique = pd.read_csv("techniques_cleaned.csv")
df_association = pd.read_csv("association_culture_technique.csv")


print("Colonnes utilisées pour l'entraînement :", df_culture.columns.tolist())


print(f"Dimensions de df_culture: {df_culture.shape}")
print(f"Dimensions de df_technique: {df_technique.shape}")
print(f"Dimensions de df_association: {df_association.shape}")


print("Distribution des techniques dans df_association:")
print(df_association['technique'].value_counts())


df_combined = df_culture.merge(df_association, left_on='nom', right_on='culture', how='inner')

X = df_combined[['cycle_croissance_jours', 'zone_culture_recommandee', 'type_sol_prefere']]
y = df_combined['technique']  


X['zone_culture_recommandee'] = X['zone_culture_recommandee'].astype(str)
X['type_sol_prefere'] = X['type_sol_prefere'].astype(str)


print(f"Dimensions de X: {X.shape}")
print(f"Dimensions de y: {y.shape}")

numeric_features = ['cycle_croissance_jours']
categorical_features = ['zone_culture_recommandee', 'type_sol_prefere']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(), categorical_features)
    ]
)

k_values = [3, 5, 7, 9]  
best_k = None
best_score = 0

model_pipeline = Pipeline(steps=[('preprocessor', preprocessor), 
                                  ('classifier', KNeighborsClassifier())])

for k in k_values:
    model_pipeline.set_params(classifier__n_neighbors=k)
    scores = cross_val_score(model_pipeline, X, y, cv=5)  
    mean_score = scores.mean()
    print(f"Score moyen pour K={k}: {mean_score}")

    if mean_score > best_score:
        best_score = mean_score
        best_k = k

print(f"Meilleure valeur pour K: {best_k} avec un score moyen de {best_score}")

model_pipeline.set_params(classifier__n_neighbors=best_k)
model_pipeline.fit(X, y)

joblib.dump(model_pipeline, 'trained_model.pkl')

print("Modèle entraîné et sauvegardé dans 'trained_model.pkl'.")
