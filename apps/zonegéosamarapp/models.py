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
    TEXTURE_CHOICES = [
        ('Grainy', 'Grainy'),
        ('Clayey', 'Clayey'),
        ('Loamy', 'Loamy'),
        ('Silty', 'Silty'),
        ('Sandy', 'Sandy'),
        ('Peaty', 'Peaty'),
        ('Chalky', 'Chalky'),
        ('Saline', 'Saline'),
    ]

    PROFONDEUR_CHOICES = [
        ('5 cm', '5 cm'),
        ('10 cm', '10 cm'),
        ('15 cm', '15 cm'),
        ('20 cm', '20 cm'),
        ('25 cm', '25 cm'),
        ('30 cm', '30 cm'),
        ('35 cm', '35 cm'),
        ('40 cm', '40 cm'),
    ]

    CAPACITE_RETENUE_EAU_CHOICES = [
        ('Very Low', 'Very Low'),
        ('Low', 'Low'),
        ('Moderate', 'Moderate'),
        ('High', 'High'),
        ('Very High', 'Very High'),
        ('Extreme', 'Extreme'),
        ('Saturated', 'Saturated'),
        ('Variable', 'Variable'),
    ]

    NUTRIMENTS_DISPONIBLES_CHOICES = [
        ('Nitrogen, Phosphorus', 'Nitrogen, Phosphorus'),
        ('Potassium, Calcium', 'Potassium, Calcium'),
        ('Magnesium, Sulfur', 'Magnesium, Sulfur'),
        ('Iron, Zinc', 'Iron, Zinc'),
        ('Copper, Manganese', 'Copper, Manganese'),
        ('Boron, Molybdenum', 'Boron, Molybdenum'),
        ('Calcium, Magnesium', 'Calcium, Magnesium'),
        ('Organic Matter', 'Organic Matter'),
    ]

    nomTypeSol = models.CharField(max_length=50)
    texture = models.CharField(max_length=50, choices=TEXTURE_CHOICES, blank=True, null=True)
    profondeur = models.CharField(max_length=50, choices=PROFONDEUR_CHOICES, blank=True, null=True)
    pH = models.DecimalField(max_digits=4, decimal_places=2)
    capacite_retenue_eau = models.CharField(max_length=50, choices=CAPACITE_RETENUE_EAU_CHOICES, blank=True, null=True)
    nutriments_disponibles = models.CharField(max_length=50, choices=NUTRIMENTS_DISPONIBLES_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.nomTypeSol
    
   
