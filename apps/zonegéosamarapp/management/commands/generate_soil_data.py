import random
from faker import Faker
from django.core.management.base import BaseCommand
from apps.zonegéosamarapp.models import TypeDeSol

class Command(BaseCommand):
    help = 'Generate random soil data'

    def handle(self, *args, **kwargs):
        self.generate_random_soil_data(500) 

    def generate_random_soil_data(self, num_samples):
        fake = Faker()

        textures = [choice[0] for choice in TypeDeSol.TEXTURE_CHOICES]
        profondeurs = [choice[0] for choice in TypeDeSol.PROFONDEUR_CHOICES]
        capacite_retention_eau = [choice[0] for choice in TypeDeSol.CAPACITE_RETENUE_EAU_CHOICES]
        nutriments_disponibles = [choice[0] for choice in TypeDeSol.NUTRIMENTS_DISPONIBLES_CHOICES]

        for _ in range(num_samples):
            texture = random.choice(textures)
            profondeur = random.choice(profondeurs)
            pH = round(random.uniform(4.0, 8.5), 2)  # pH between 4.0 and 8.5
            capacite = random.choice(capacite_retention_eau)
            nutriments = random.choice(nutriments_disponibles)
            
            TypeDeSol.objects.create(
                nomTypeSol=fake.word(),
                texture=texture,
                profondeur=profondeur,
                pH=pH,
                capacite_retenue_eau=capacite,
                nutriments_disponibles=nutriments
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {num_samples} samples of soil data.'))
