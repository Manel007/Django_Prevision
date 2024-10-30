import pandas as pd
from django.core.management.base import BaseCommand
from apps.pesticide.models import Pesticide  

class Command(BaseCommand):
    help = 'Load pesticide data from CSV file'

    def handle(self, *args, **kwargs):

        pesticide_data = pd.read_csv('C:/Users/user/Desktop/black-dashboard-django-master/black-dashboard-django-master/pesticides.csv')


        pesticide_data.columns = pesticide_data.columns.str.strip()  

        print("DataFrame columns:", pesticide_data.columns)

        for _, row in pesticide_data.iterrows():
            Pesticide.objects.create(
                domain=row['domain'],
                area=row['area'],
                element=row['element'],
                item=row['item'],
                year=int(row['year']),
                unit=row['unit'],
                value=float(row['value'])  
            )

        self.stdout.write(self.style.SUCCESS('Pesticide data loaded successfully.'))
