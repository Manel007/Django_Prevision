import pandas as pd

# Remplace 'path_to_your_file.csv' par le chemin vers ton fichier
file_path = 'techniques.csv'  # Ou 'cultures.csv'

# Charge le fichier CSV dans un DataFrame
df = pd.read_csv(file_path)

# Affiche les 10 premières lignes
print(df.head())

# Affiche les colonnes du DataFrame pour vérifier les noms
print(df.columns)
