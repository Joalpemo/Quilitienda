# Generated by Django 3.2.6 on 2021-12-01 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quilitienda', '0011_alter_customer_apellido'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='address',
            new_name='direccion',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='city',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='state',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='zipcode',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='departamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Quilitienda.departamento'),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='municipio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Quilitienda.municipio'),
        ),
    ]
