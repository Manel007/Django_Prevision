# scripts/import_data.py

import os
import sys

# Chemin vers le projet Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

import csv
from django.utils.dateparse import parse_date
from apps.Culture.models import CultureAgricole
from apps.Technique.models import TechniqueCulture

def import_cultures(culture_data):
    """Importe les cultures à partir des données."""
    for row in culture_data:
        try:
            # Ajout d'une vérification pour s'assurer que les valeurs nécessaires sont présentes
            if not row['cycle_croissance_jours']:
                print(f"Cycle de croissance manquant pour la culture: {row['nom']}. Culture non ajoutée.")
                continue  # Passe à la culture suivante si la valeur est manquante
            
            culture, created = CultureAgricole.objects.get_or_create(
                nom=row['nom'],
                defaults={
                    'description': row['description'],
                    'cycle_croissance_jours': int(row['cycle_croissance_jours']),
                    'rendement_attendu': float(row['rendement_attendu']),
                    'zone_culture_recommandee': row['zone_culture_recommandee'],
                    'type_sol_prefere': row['type_sol_prefere'],
                    'irrigation': row['irrigation']
                }
            )
            if created:
                print(f"Culture ajoutée: {culture.nom}")
            else:
                print(f"Culture existante: {culture.nom}")
        except Exception as e:
            print(f"Erreur lors de l'importation de la culture {row['nom']}: {e}")

def import_techniques(technique_data):
    """Importe les techniques à partir des données."""
    for row in technique_data:
        try:
            technique = TechniqueCulture.objects.create(
                nom_technique=row['nom_technique'],
                description=row['description'],
                date_application=parse_date(row['date_application']),
                impact_rendement=float(row['impact_rendement'])
            )
            # Associer la technique à la culture correspondante
            culture_name = row['culture_id']
            print(f"Tentative de trouver la culture: {culture_name}")
            try:
                culture = CultureAgricole.objects.get(nom=culture_name)
                technique.cultures_associees.add(culture)
                print(f"Technique ajoutée: {technique.nom_technique} associée à {culture.nom}")
            except CultureAgricole.DoesNotExist:
                print(f"Culture '{culture_name}' n'existe pas, ajout de la culture...")
                # Ajouter la culture manquante avec des valeurs par défaut
                culture = CultureAgricole.objects.create(
                    nom=culture_name,
                    description='',  # Valeur par défaut si non fournie
                    cycle_croissance_jours=0,  # Valeur par défaut
                    rendement_attendu=0.0,  # Valeur par défaut
                    zone_culture_recommandee='',  # Valeur par défaut
                    type_sol_prefere='',  # Valeur par défaut
                    irrigation=''  # Valeur par défaut
                )
                technique.cultures_associees.add(culture)
                print(f"Cultures ajoutée: {culture.nom}")
                print(f"Technique ajoutée: {technique.nom_technique} associée à {culture.nom}")
        except Exception as e:
            print(f"Erreur lors de l'importation de la technique {row['nom_technique']}: {e}")

def read_csv(file_path):
    """Lit le fichier CSV et renvoie les données sous forme de liste de dictionnaires."""
    with open(file_path, newline='') as csvfile:
        return list(csv.DictReader(csvfile))

if __name__ == "__main__":
    culture_data = read_csv('scripts/cultures.csv')
    technique_data = read_csv('scripts/techniques.csv')

    import_cultures(culture_data)
    import_techniques(technique_data)