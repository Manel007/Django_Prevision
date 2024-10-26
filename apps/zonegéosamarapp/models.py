# models.py
from django.db import models

# Create your models here.
class ZoneGeographique(models.Model):
    nomZone = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    annee = models.PositiveIntegerField()
    temperatureMoyenne = models.DecimalField(max_digits=5, decimal_places=2)
    pluviometrie = models.DecimalField(max_digits=6, decimal_places=2)

    # Relation avec TypeDeSol one to one
    type_de_sol = models.ForeignKey('TypeDeSol', on_delete=models.CASCADE) 

    def __str__(self):
        return self.nomZone


class TypeDeSol(models.Model):

    nomTypeSol = models.CharField(max_length=50)
    texture = models.CharField(max_length=50, blank=True, null=True)
    profondeur = models.CharField(max_length=50,  blank=True, null=True)
    pH =  models.DecimalField(max_digits=4, decimal_places=2)
    capacite_retenue_eau = models.CharField(max_length=50, blank=True, null=True)
    nutriments_disponibles = models.CharField(max_length=50, blank=True, null=True)

 #culture_recommandee = Column(String, nullable=True)  # culture Recommandée
    def __str__(self):
        return self.nomTypeSol

    
   
