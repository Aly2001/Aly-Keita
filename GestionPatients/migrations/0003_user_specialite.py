# Generated by Django 5.0.3 on 2024-06-06 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionPatients', '0002_alter_user_date_naissance'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='specialite',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
