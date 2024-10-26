from django.db import models

# Create your models here.
class ZoneGeographique(models.Model):
   
    nomZone = models.CharField(max_length=100, unique=True)  # Nom de la zone
    description = models.TextField(blank=True, null=True)  # Description optionnelle (caractéristiques du terrain)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # Latitude de la zone
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # Longitude de la zone

    annee = models.PositiveIntegerField()  # Année de référence pour les données météorologiques
    temperatureMoyenne = models.DecimalField(max_digits=5, decimal_places=2)  # Température moyenne annuelle (°C)
    pluviometrie = models.DecimalField(max_digits=6, decimal_places=2)  # Pluviométrie annuelle totale (mm)
    
def __str__(self):
        return self.nomZone