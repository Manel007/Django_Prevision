# Generated by Django 4.2 on 2024-10-30 00:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RessourceEntity', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ressource',
            name='fournisseur',
        ),
    ]
