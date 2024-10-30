import pandas as pd

nouvelles_donnees = {
    'cycle_croissance_jours': [30, 45, 60, 50, 70],
    'rendement_attendu': [5, 7, 8, 6, 10],
    'impact_rendement': [1, 2, 3, 4, 5],  
    'type_sol_prefere': ['Argileux', 'Limoneux', 'Sableux', 'Argileux', 'Limoneux'],
    'irrigation': ['Modérée', 'Élevée', 'Faible', 'Modérée', 'Élevée']
}

df_nouvelles_donnees = pd.DataFrame(nouvelles_donnees)

df_nouvelles_donnees.to_csv('nouvelles_donnees.csv', index=False)
