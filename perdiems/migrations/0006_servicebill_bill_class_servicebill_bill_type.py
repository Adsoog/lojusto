# Generated by Django 5.1.4 on 2024-12-30 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perdiems', '0005_requestservice_motive_alter_servicebill_bill_ruc'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicebill',
            name='bill_class',
            field=models.CharField(blank=True, choices=[('SERVICIO', 'Servicio'), ('PRODUCTO', 'Producto')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='servicebill',
            name='bill_type',
            field=models.CharField(blank=True, choices=[('FACTURA', 'Factura'), ('BOLETA', 'Boleta'), ('RECIBO', 'Recibo')], max_length=20, null=True),
        ),
    ]
