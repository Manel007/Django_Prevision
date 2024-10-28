from django.db import models

from apps.Culture.models import CultureAgricole

class TechniqueCulture(models.Model):
    nom_technique = models.CharField(max_length=100)
    description = models.TextField()
    cultures_associees = models.ManyToManyField(CultureAgricole)  
    date_application = models.TextField()
    impact_rendement = models.FloatField()

    def __str__(self):
        return self.nom_technique