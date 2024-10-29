import pandas as pd
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from ..models import Pesticide

class Command(BaseCommand):
    help = 'Add selected pesticide data to CSV file'

    def add_arguments(self, parser):
        parser.add_argument('selected_ids', nargs='+', type=int, help='List of selected pesticide IDs to add to the CSV.')

    def handle(self, *args, **kwargs):
        selected_ids = kwargs['selected_ids']

        # Charger les données existantes dans le fichier CSV
        try:
            pesticide_data = pd.read_csv('C:/Users/ASUS/Desktop/django/Django_Prevision/pesticides.csv')
        except FileNotFoundError:
            pesticide_data = pd.DataFrame(columns=['Domain', 'Area', 'Element', 'Item', 'Year', 'Unit', 'Value'])

        # Récupérer les pesticides correspondants aux IDs sélectionnés
        for pesticide_id in selected_ids:
            try:
                pesticide = get_object_or_404(Pesticide, id=pesticide_id)
                new_row = {
                    'Domain': pesticide.domain,        # Doit correspondre à la première colonne
                    'Area': pesticide.area,            # Deuxième colonne
                    'Element': pesticide.element,      # Troisième colonne
                    'Item': pesticide.item,            # Quatrième colonne
                    'Year': pesticide.year,            # Cinquième colonne
                    'Unit': pesticide.unit,            # Sixième colonne
                    'Value': pesticide.value           # Septième colonne
                }

                # Vérifiez que les valeurs nécessaires ne sont pas vides
                if all(new_row.values()):  # S'assure que toutes les valeurs ne sont pas nulles
                    pesticide_data = pesticide_data.append(new_row, ignore_index=True)
                else:
                    self.stdout.write(self.style.WARNING(f'Les données pour le pesticide ID {pesticide_id} sont incomplètes.'))

            except Http404:
                self.stdout.write(self.style.WARNING(f'Pesticide with ID {pesticide_id} does not exist.'))

        # Vérifiez si le DataFrame est toujours vide avant d'enregistrer
        if not pesticide_data.empty:
            # Enregistrer le DataFrame mis à jour dans le fichier CSV
            pesticide_data.to_csv('C:/Users/ASUS/Desktop/django/Django_Prevision/pesticides.csv', index=False)
            self.stdout.write(self.style.SUCCESS('Selected pesticide data added to the CSV successfully.'))
        else:
            self.stdout.write(self.style.WARNING('Aucune donnée à ajouter au fichier CSV.'))
