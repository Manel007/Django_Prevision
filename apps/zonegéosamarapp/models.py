from django.db import models

# Create your models here.
class ZoneGeographique(models.Model):
   
    nomZone = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)  
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  

    annee = models.PositiveIntegerField() 
    temperatureMoyenne = models.DecimalField(max_digits=5, decimal_places=2) 
    pluviometrie = models.DecimalField(max_digits=6, decimal_places=2)  
    
def __str__(self):
        return self.nomZone