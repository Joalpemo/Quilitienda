# Generated by Django 3.2.6 on 2021-11-25 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quilitienda', '0006_auto_20211124_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='departamento',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Quilitienda.customer'),
        ),
    ]
