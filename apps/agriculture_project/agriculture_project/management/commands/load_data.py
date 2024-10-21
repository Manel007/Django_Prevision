import pandas as pd
from django.core.management.base import BaseCommand
from ...models import CropYield  # Adjust the number of dots based on the directory structure

class Command(BaseCommand):
    help = 'Load data from CSV files'

    def handle(self, *args, **kwargs):
        # Load yield data
        yield_data = pd.read_csv('C:/Users/user/Desktop/black-dashboard-django-master/black-dashboard-django-master/yield_df.csv')

        # Clean column names
        yield_data.columns = yield_data.columns.str.strip()  # Remove leading/trailing whitespace

        # Print columns to check for correctness
        print("DataFrame columns:", yield_data.columns)

        for _, row in yield_data.iterrows():
            CropYield.objects.create(
                area=row['Area'],
                item=row['Item'],
                year=int(row['Year']),
                hg_per_ha_yield=float(row['hg/ha_yield']),  # Update this line to access the correct column
                average_rain_fall=0,  # To be filled in with additional data
                pesticides_tonnes=0,   # To be filled in with additional data
                avg_temp=0             # To be filled in with additional data
            )

        self.stdout.write(self.style.SUCCESS('Data loaded successfully.'))
