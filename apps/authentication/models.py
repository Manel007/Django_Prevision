# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.db import models

class Culture(models.Model):
    id = models.BigAutoField(primary_key=True)  # Use BigAutoField or AutoField as needed
    nom = models.CharField(max_length=100)
    type_culture = models.CharField(max_length=100)
    duree_croissance = models.IntegerField()
    superficie_requise = models.FloatField()
    conditions_optimales = models.JSONField()  # or any other field type you require

    def __str__(self):
        return self.nom
