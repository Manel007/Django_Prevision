import pandas as pd
from django.core.management.base import BaseCommand
from apps.pesticide.models import Pesticide  

class Command(BaseCommand):
    help = 'Load pesticide data from CSV file'

    def handle(self, *args, **kwargs):
        # Load pesticide data from the specified CSV file
        try:
            pesticide_data = pd.read_csv('C:/Users/user/Desktop/black-dashboard-django-master/black-dashboard-django-master/pesticides.csv')
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('The specified CSV file was not found.'))
            return
        
        # Strip whitespace from column names
        pesticide_data.columns = pesticide_data.columns.str.strip()  
        
        # Print the column names for debugging
        print("DataFrame columns:", pesticide_data.columns.tolist())

        for _, row in pesticide_data.iterrows():
            try:
                # Create a new Pesticide object for each row
                Pesticide.objects.create(
                    domain=row['Domain'],      # Adjust to match the actual CSV header
                    area=row['Area'],          # Adjust to match the actual CSV header
                    element=row['Element'],    # Adjust to match the actual CSV header
                    item=row['Item'],          # Adjust to match the actual CSV header
                    year=int(row['Year']),     # Adjust to match the actual CSV header
                    unit=row['Unit'],          # Adjust to match the actual CSV header
                    value=float(row['Value'])  # Adjust to match the actual CSV header
                )
            except KeyError as e:
                self.stdout.write(self.style.ERROR(f'Missing column in row: {e}'))
            except ValueError as e:
                self.stdout.write(self.style.ERROR(f'Value error in row: {e}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))

        self.stdout.write(self.style.SUCCESS('Pesticide data loaded successfully.'))
