from django.db import models

# Modèle Ressource
class Ressource(models.Model):
    TYPE_RESSOURCE_CHOICES = [
        ('eau', 'Eau'),
        ('engrais', 'Engrais'),
        ('pesticide', 'Pesticide'),
        ('carburant', 'Carburant'),
        ('semences', 'Semences'),
    ]
    nom_ressource = models.CharField(max_length=100, verbose_name="Nom de la ressource")
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


# Modèle Fournisseur
class Fournisseur(models.Model):
    TYPE_FOURNISSEUR_CHOICES = [
        ('importateur', 'Importateur'),
        ('grossiste', 'Grossiste'),
        ('entreprise_prive', 'Entreprise Privée'),
        ('cooperative_agricole', 'Coopérative Agricole'),
    ]

    nom = models.CharField(max_length=100, verbose_name="Nom du fournisseur")
    type_fournisseur = models.CharField(
        max_length=20, 
        choices=TYPE_FOURNISSEUR_CHOICES, 
        verbose_name="Type de fournisseur"
    )
    adresse = models.TextField(verbose_name="Adresse du fournisseur")
    numero_telephone = models.CharField(max_length=15, verbose_name="Numéro de téléphone")
    ressources_fournies = models.ManyToManyField(
        Ressource, 
        through='FournisseurRessource', 
        verbose_name="Ressources fournies"
    )
    quantite_disponible = models.FloatField(verbose_name="Quantité disponible", default=0)

    def __str__(self):
        return f"{self.nom} ({self.get_type_fournisseur_display()})"


# Modèle intermédiaire FournisseurRessource
class FournisseurRessource(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('fournisseur', 'ressource')

    def __str__(self):
        return f"{self.fournisseur.nom} - {self.ressource.type_ressource} ({self.quantite_disponible})"
