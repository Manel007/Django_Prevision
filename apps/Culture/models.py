from django.db import models

class CultureAgricole(models.Model):
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    cycle_croissance_jours = models.IntegerField()
    rendement_attendu = models.FloatField()
    zone_culture_recommandee = models.CharField(max_length=100)
    type_sol_prefere = models.CharField(max_length=100)
    irrigation = models.CharField(max_length=100)

    def __str__(self):
        return self.nom