# Generated by Django 3.2.6 on 2021-11-26 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quilitienda', '0008_auto_20211125_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='municipio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Quilitienda.municipio'),
        ),
    ]
