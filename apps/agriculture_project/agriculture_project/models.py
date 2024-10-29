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

class Review(models.Model):
    crop_yield = models.ForeignKey(CropYield, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()  # For example, from 1 to 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('archived', 'Archived')
    ], default='active')
    def __str__(self):
        return f"Review on {self.crop_yield} with rating {self.rating}"
