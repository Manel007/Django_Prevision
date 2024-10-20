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
class PesticideUse(models.Model):
    area = models.CharField(max_length=255)
    year = models.IntegerField()
    unit = models.CharField(max_length=255)
    value = models.FloatField()

    def __str__(self):
        return f"{self.area} - {self.year} - {self.value}"

class RainfallData(models.Model):
    area = models.CharField(max_length=255)
    year = models.IntegerField()
    average_rainfall = models.FloatField()

    def __str__(self):
        return f"{self.area} - {self.year} - {self.average_rainfall}"

class YieldData(models.Model):
    area = models.CharField(max_length=255)
    item = models.CharField(max_length=255)
    year = models.IntegerField()
    yield_hg_per_ha = models.FloatField()
    average_rainfall = models.FloatField()
    pesticides_used = models.FloatField()
    avg_temp = models.FloatField()

    def __str__(self):
        return f"{self.area} - {self.item} - {self.year} - {self.yield_hg_per_ha}"



