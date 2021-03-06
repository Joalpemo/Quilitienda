# Generated by Django 3.2.6 on 2021-12-01 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quilitienda', '0009_customer_municipio'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='documento',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='apellido',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='celular',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
