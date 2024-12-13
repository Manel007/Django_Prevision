# Generated by Django 4.2 on 2024-10-25 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CultureAgricole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('cycle_croissance_jours', models.IntegerField()),
                ('rendement_attendu', models.FloatField()),
                ('zone_culture_recommandee', models.CharField(max_length=100)),
                ('type_sol_prefere', models.CharField(max_length=100)),
                ('irrigation', models.CharField(max_length=100)),
            ],
        ),
    ]
