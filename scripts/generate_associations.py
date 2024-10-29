import pandas as pd

# Chargement des fichiers de cultures et de techniques
df_culture = pd.read_csv('cultures_cleaned.csv')
df_technique = pd.read_csv('techniques_cleaned.csv')

# Afficher les noms des colonnes
print("Colonnes de df_culture:", df_culture.columns)
print("Colonnes de df_technique:", df_technique.columns)

# Pour l'exemple, nous allons créer un fichier d'association vide
# Assurez-vous que le fichier d'association existe
associations = []

# Boucle pour associer chaque culture à chaque technique
for culture_index, culture_row in df_culture.iterrows():
    culture_name = culture_row['nom']  # Nom de la culture

    for technique_index, technique_row in df_technique.iterrows():
        technique_name = technique_row['nom_technique']  # Nom de la technique

        # Ici, vous pouvez appliquer une logique pour décider quelles techniques s'associent à quelles cultures
        # Pour cet exemple, nous allons les associer toutes
        associations.append({
            'culture': culture_name,
            'technique': technique_name
        })

# Convertir les associations en DataFrame
df_associations = pd.DataFrame(associations)

# Enregistrer les associations dans un fichier CSV
df_associations.to_csv('association_culture_technique.csv', index=False)

print("Associations enregistrées dans 'association_culture_technique.csv'.")
