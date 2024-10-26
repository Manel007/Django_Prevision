from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ressource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'type_ressource',
                    models.CharField(
                        max_length=50, 
                        choices=[
                            ('eau', 'Eau'),
                            ('engrais', 'Engrais'),
                            ('pesticide', 'Pesticide'),
                            ('carburant', 'Carburant'),
                            ('semences', 'Semences'),
                        ],
                        verbose_name='Type de ressource'
                    )
                ),
                (
                    'quantite',
                    models.FloatField(verbose_name='Quantité disponible')
                ),
                (
                    'unite_mesure',
                    models.CharField(max_length=20, verbose_name='Unité de mesure')
                ),
                (
                    'zone',
                    models.CharField(max_length=100, verbose_name="Zone d’application")
                ),
            ],
        ),
    ]
