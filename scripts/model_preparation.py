import pandas as pd
import random

df_cultures = pd.read_csv('scripts/cultures.csv')
df_techniques = pd.read_csv('scripts/techniques.csv')

print("Aperçu des cultures:")
print(df_cultures.head())
print("Aperçu des techniques:")
print(df_techniques.head())

df_cultures.columns = df_cultures.columns.str.strip().str.lower()  # Normalisation des colonnes
df_techniques.columns = df_techniques.columns.str.strip().str.lower()


print("Valeurs uniques dans df_cultures['zone_culture_recommandee']:", df_cultures['zone_culture_recommandee'].unique())
print("Valeurs uniques dans df_techniques['impact_rendement']:", df_techniques['impact_rendement'].unique())

associations = []

for culture_index, culture_row in df_cultures.iterrows():
    culture_name = culture_row['nom']  

    selected_techniques = random.sample(df_techniques['nom_technique'].tolist(), k=random.randint(2, 3))
    
    for technique_name in selected_techniques:
        associations.append({
            'culture': culture_name,
            'technique': technique_name
        })

df_associations = pd.DataFrame(associations)

df_cultures.to_csv('cultures_cleaned.csv', index=False)
df_techniques.to_csv('techniques_cleaned.csv', index=False)
df_associations.to_csv('association_culture_technique.csv', index=False)

print("Fichiers nettoyés et d'association sauvegardés.")
