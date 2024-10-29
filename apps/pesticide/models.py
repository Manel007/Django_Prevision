from django.db import models


class Pesticide(models.Model):
    domain = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    element = models.CharField(max_length=100)
    item = models.CharField(max_length=100)
    year = models.IntegerField()
    unit = models.CharField(max_length=100)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.area} pesticide in {self.year} for {self.area}"
