
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

def generate_cultures(n):
    cultures = []
    types_sol = ["Sablonneux", "Argileux", "Limoneux"]
    irrigations = ["Faible", "Modérée", "Élevée"]
    zones = ["Nord", "Sud", "Est", "Ouest"]

    for _ in range(n):
        cultures.append({
            "nom": fake.word().capitalize(),
            "description": fake.sentence(nb_words=5),
            "cycle_croissance_jours": random.randint(60, 180),
            "rendement_attendu": round(random.uniform(3, 10), 2),
            "zone_culture_recommandee": random.choice(zones),
            "type_sol_prefere": random.choice(types_sol),
            "irrigation": random.choice(irrigations)
        })
    return pd.DataFrame(cultures)

def generate_techniques(n, culture_ids):
    techniques = []
    for _ in range(n):
        techniques.append({
            "nom_technique": fake.bs().capitalize(),
            "description": fake.sentence(nb_words=10),
            "date_application": fake.date_this_year(),
            "impact_rendement": round(random.uniform(0.8, 1.5), 2),
            "culture_id": random.choice(culture_ids)
        })
    return pd.DataFrame(techniques)

# Générer les cultures et techniques
cultures_df = generate_cultures(100)  # 50 cultures
cultures_df.to_csv('cultures.csv', index=False)  # Enregistrer dans un fichier CSV

techniques_df = generate_techniques(200, cultures_df.index.tolist())  # 100 techniques associées
techniques_df.to_csv('techniques.csv', index=False)  # Enregistrer dans un fichier CSV

print("Données générées et enregistrées dans 'cultures.csv' et 'techniques.csv'")
