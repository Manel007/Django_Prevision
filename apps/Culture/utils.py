# utils.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd

# Exemple de données de caractéristiques textuelles
data = {
    'culture': ['Blé', 'Maïs', 'Tomate', 'Pomme de terre', 'Riz'],
    'type_sol': ['Argile', 'Sable', 'Argile', 'Limoneux', 'Inondé'],
    'irrigation': ['Goutte à goutte', 'Aspersion', 'Goutte à goutte', 'Inondation', 'Aspersion'],
    'zone_geographique': ['Europe', 'Amérique', 'Europe', 'Asie', 'Asie']
}

df = pd.DataFrame(data)

# Concaténer les caractéristiques textuelles pour chaque culture
df['features'] = df['type_sol'] + ' ' + df['irrigation'] + ' ' + df['zone_geographique']

# Utiliser TF-IDF pour encoder les caractéristiques textuelles
tfidf = TfidfVectorizer()
features_matrix = tfidf.fit_transform(df['features'])

# Entraînement du modèle k-Nearest Neighbors
k = 5  # Nombre de voisins à considérer
knn_model = NearestNeighbors(n_neighbors=k, metric='cosine')
knn_model.fit(features_matrix)

def recommend_technique(new_culture_features):
    new_culture_features_tfidf = tfidf.transform([new_culture_features])
    _, indices = knn_model.kneighbors(new_culture_features_tfidf)
    return indices