from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Agriculteur(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    contact = models.CharField(max_length=8)
    adresse = models.CharField(max_length=100)
    region = models.CharField(max_length=50)


    def __str__(self):
        return f'Agriculteur: {self.nom} {self.prenom}'

