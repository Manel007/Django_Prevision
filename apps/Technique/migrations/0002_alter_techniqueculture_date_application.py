# Generated by Django 4.2 on 2024-10-28 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Technique', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='techniqueculture',
            name='date_application',
            field=models.TextField(null=True),
        ),
    ]
