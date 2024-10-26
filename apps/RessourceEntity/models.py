from django.db import models

class Ressource(models.Model):
    TYPE_RESSOURCE_CHOICES = [
        ('eau', 'Eau'),
        ('engrais', 'Engrais'),
        ('pesticide', 'Pesticide'),
        ('carburant', 'Carburant'),
        ('semences', 'Semences'),
    ]

    type_ressource = models.CharField(
        max_length=50, 
        choices=TYPE_RESSOURCE_CHOICES, 
        verbose_name="Type de ressource"
    )
    quantite = models.FloatField(verbose_name="Quantité disponible")
    unite_mesure = models.CharField(max_length=20, verbose_name="Unité de mesure")
    zone = models.CharField(max_length=100, verbose_name="Zone d’application")

    def __str__(self):
        return f"{self.type_ressource} - {self.quantite} {self.unite_mesure} ({self.zone})"
