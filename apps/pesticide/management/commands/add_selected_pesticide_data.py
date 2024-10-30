import pandas as pd
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from django.http import Http404  # Import Http404
from apps.pesticide.models import Pesticide  

class Command(BaseCommand):
    help = 'Add selected pesticide data to CSV file'

    def add_arguments(self, parser):
        parser.add_argument('selected_ids', nargs='+', type=int, help='List of selected pesticide IDs to add to the CSV.')

    def handle(self, *args, **kwargs):
        selected_ids = kwargs['selected_ids']

        # Read existing pesticide data or create a new DataFrame if the file doesn't exist
        try:
            pesticide_data = pd.read_csv('C:/Users/user/Desktop/black-dashboard-django-master/black-dashboard-django-master/pesticides.csv')
        except FileNotFoundError:
            pesticide_data = pd.DataFrame(columns=['Domain', 'Area', 'Element', 'Item', 'Year', 'Unit', 'Value'])

        # Create a list to hold new rows
        new_rows = []

        for pesticide_id in selected_ids:
            try:
                pesticide = get_object_or_404(Pesticide, id=pesticide_id)
                new_row = {
                    'Domain': pesticide.domain,        
                    'Area': pesticide.area,           
                    'Element': pesticide.element,     
                    'Item': pesticide.item,            
                    'Year': pesticide.year,            
                    'Unit': pesticide.unit,          
                    'Value': pesticide.value          
                }

                if all(new_row.values()):  
                    new_rows.append(new_row)  # Add new row to the list
                else:
                    self.stdout.write(self.style.WARNING(f'Les données pour le pesticide ID {pesticide_id} sont incomplètes.'))

            except Http404:
                self.stdout.write(self.style.WARNING(f'Pesticide with ID {pesticide_id} does not exist.'))

        # If we have new rows, append them to the DataFrame
        if new_rows:
            new_rows_df = pd.DataFrame(new_rows)
            pesticide_data = pd.concat([pesticide_data, new_rows_df], ignore_index=True)

            # Save updated DataFrame back to CSV
            pesticide_data.to_csv('C:/Users/user/Desktop/black-dashboard-django-master/black-dashboard-django-master/pesticides.csv', index=False)

            self.stdout.write(self.style.SUCCESS('Selected pesticide data added to the CSV successfully.'))
        else:
            self.stdout.write(self.style.WARNING('Aucune donnée à ajouter au fichier CSV.'))
