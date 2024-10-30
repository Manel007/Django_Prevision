import pandas as pd

df_culture = pd.read_csv('cultures_cleaned.csv')
df_technique = pd.read_csv('techniques_cleaned.csv')

print("Colonnes de df_culture:", df_culture.columns)
print("Colonnes de df_technique:", df_technique.columns)


associations = []

for culture_index, culture_row in df_culture.iterrows():
    culture_name = culture_row['nom'] 

    for technique_index, technique_row in df_technique.iterrows():
        technique_name = technique_row['nom_technique']  


        associations.append({
            'culture': culture_name,
            'technique': technique_name
        })

df_associations = pd.DataFrame(associations)

df_associations.to_csv('association_culture_technique.csv', index=False)

print("Associations enregistrées dans 'association_culture_technique.csv'.")
