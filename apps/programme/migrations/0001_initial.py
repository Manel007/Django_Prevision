# Generated by Django 5.1.2 on 2024-10-27 07:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pesticide', '0002_rename_item_pesticide_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgrammeDeTraitement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('frequence_application', models.CharField(choices=[('hebdomadaire', 'Hebdomadaire'), ('mensuel', 'Mensuel'), ('annuel', 'Annuel')], default='mensuel', max_length=50)),
                ('pesticide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programmes_de_traitement', to='pesticide.pesticide')),
            ],
        ),
    ]