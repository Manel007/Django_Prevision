import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Charger les données
data = pd.read_csv('Ressourcee.csv')  # Mettez à jour le chemin de votre fichier CSV

# Visualiser les premières lignes pour comprendre la structure
print(data.head())

# Vérifier les valeurs manquantes
print(data.isnull().sum())

# Remplir ou supprimer les valeurs manquantes si nécessaire
# data.fillna(0, inplace=True)  # Exemple de remplissage
# data.dropna(inplace=True)  # Exemple de suppression

# Sélectionner les caractéristiques (features) et la cible (target)
X = data[['nom_ressource','Saison']]  # Remplacez par les noms de vos caractéristiques
y = data['quantite']  # La variable cible

# Appliquer one-hot encoding sur les caractéristiques
X = pd.get_dummies(X, drop_first=True)

# Diviser le jeu de données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Créer le modèle
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Entraîner le modèle
model.fit(X_train, y_train)

# Prédire les quantités pour l'ensemble de test
y_pred = model.predict(X_test)

# Évaluer le modèle
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Erreur quadratique moyenne : {mse}")
print(f"Coefficient de détermination R^2 : {r2}")

# Exemple de nouvelles données pour prédire la quantité
new_data = pd.get_dummies(pd.DataFrame([["Engrais liquide", "winter"]], columns=['nom_ressource', 'Saison']), drop_first=True)

# S'assurer que les nouvelles données ont les mêmes colonnes que les données d'entraînement
new_data = new_data.reindex(columns=X.columns, fill_value=0)

# Prédire la quantité
predicted_quantity = model.predict(new_data)

print(f"Quantité prédite : {predicted_quantity[0]}")
