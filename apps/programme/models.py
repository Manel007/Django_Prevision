from django.db import models
from apps.pesticide.models import Pesticide  

class ProgrammeDeTraitement(models.Model):
    nom = models.CharField(max_length=100)

    description = models.TextField()

    frequence_application = models.CharField(
        max_length=50,
        choices=[
            ('hebdomadaire', 'Hebdomadaire'),
            ('mensuel', 'Mensuel'),
            ('annuel', 'Annuel')
        ],
        default='mensuel'
    )
    
    pesticide = models.ForeignKey(Pesticide, on_delete=models.CASCADE, related_name='programmes_de_traitement')

    def __str__(self):
        return f"{self.nom} - {self.pesticide.nom}"