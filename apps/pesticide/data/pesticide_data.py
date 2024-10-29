import pandas as pd
from django.core.management.base import BaseCommand
from ..models import Pesticide  

class Command(BaseCommand):
    help = 'Load pesticide data from CSV file'

    def handle(self, *args, **kwargs):
        # Charger les données des pesticides
        pesticide_data = pd.read_csv('C:/Users/rebhi/OneDrive/Bureau/Django_Prevision/pesticides.csv')

        # Nettoyer les noms de colonnes
        pesticide_data.columns = pesticide_data.columns.str.strip()  # Supprimer les espaces

        # Vérifier les colonnes pour s'assurer qu'elles sont correctes
        print("DataFrame columns:", pesticide_data.columns)

        for _, row in pesticide_data.iterrows():
            Pesticide.objects.create(
                domain=row['domain'],
                area=row['area'],
                element=row['element'],
                item=row['item'],
                year=int(row['year']),
                unit=row['unit'],
                value=float(row['value'])  # Assurez-vous que cette colonne existe
            )

        self.stdout.write(self.style.SUCCESS('Pesticide data loaded successfully.'))
