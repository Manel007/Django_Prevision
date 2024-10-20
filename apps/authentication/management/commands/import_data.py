import pandas as pd
from django.core.management.base import BaseCommand
from apps.authentication.models import Culture

class Command(BaseCommand):
    help = 'Import data from CSV files into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Importing data...'))

        # Paths to CSV files
        csv_files = [
            'C:/Users/user/Desktop/black-dashboard-django-master/black-dashboard-django-master/pesticides.csv',
            'C:/Users/user/Desktop/black-dashboard-django-master/black-dashboard-django-master/rainfall.csv',
            'C:/Users/user/Desktop/black-dashboard-django-master/black-dashboard-django-master/temp.csv',
            'C:/Users/user/Desktop/black-dashboard-django-master/black-dashboard-django-master/yield_df.csv',
            'C:/Users/user/Desktop/black-dashboard-django-master/black-dashboard-django-master/yield.csv',
        ]

        for csv_file in csv_files:
            df = pd.read_csv(csv_file)

            # Check and fill missing values
            df.fillna(0, inplace=True)

            for index, row in df.iterrows():
                try:
                    Culture.objects.create(
                        nom=row.get('Item', ''),  # Assuming 'Item' corresponds to the name of the culture
                        type_culture=row.get('Element', ''),  # Assuming 'Element' corresponds to the type of culture
                        duree_croissance=row.get('Year', 0),  # Year might be treated as growth duration, adjust if needed
                        superficie_requise=row.get('Value', 0.0),  # Assuming 'Value' corresponds to the required area
                        conditions_optimales=row.get('average_rain_fall_mm_per_year', 0)  # Adjust according to your logic
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error importing row {index}: {e}'))

        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))
