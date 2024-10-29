from django.db import models


class CropYield(models.Model):
    area = models.CharField(max_length=100)
    item = models.CharField(max_length=100)
    year = models.IntegerField()
    hg_per_ha_yield = models.FloatField()
    average_rain_fall = models.FloatField()
    pesticides_tonnes = models.FloatField()
    avg_temp = models.FloatField()

    def __str__(self):
        return f"{self.item} yield in {self.year} for {self.area}"
