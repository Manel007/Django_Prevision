# Generated by Django 4.2 on 2024-10-19 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='culture',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='culture',
            name='nom',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='culture',
            name='type_culture',
            field=models.CharField(max_length=100),
        ),
    ]
