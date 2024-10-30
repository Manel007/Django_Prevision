import pandas as pd
from django.core.management.base import BaseCommand
from ...models import CropYield

class Command(BaseCommand):
    help = 'Load data from CSV files'

    def handle(self, *args, **kwargs):

        yield_data = pd.read_csv('C:/Users/user/Desktop/black-dashboard-django-master/black-dashboard-django-master/yield_df.csv')

        yield_data.columns = yield_data.columns.str.strip()  

        crop_yields = []

        for _, row in yield_data.iterrows():
            crop_yields.append(
                CropYield(
                 
                    area=row['Area'],
                    item=row['Item'],
                    year=int(row['Year']),
                    hg_per_ha_yield=float(row['hg/ha_yield']),
                    average_rain_fall=row['average_rain_fall_mm_per_year'],  
                    pesticides_tonnes=row['pesticides_tonnes'],              
                    avg_temp=row['avg_temp']                                  
                )
            )

        CropYield.objects.bulk_create(crop_yields)

        self.stdout.write(self.style.SUCCESS('Data loaded successfully.'))
