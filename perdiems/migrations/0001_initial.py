# Generated by Django 5.1.4 on 2024-12-23 14:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('general', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(choices=[('alimentacion', 'Alimentación'), ('transporte', 'Transporte'), ('alojamiento', 'Alojamiento'), ('combustible', 'Combustible'), ('reparaciones', 'Reparaciones'), ('otros', 'Otros')], max_length=50)),
                ('amount_per_day', models.IntegerField(default=1)),
                ('type_item', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RequestService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oti', models.CharField(max_length=50)),
                ('requested_date', models.DateField(auto_now_add=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('days', models.IntegerField()),
                ('details', models.TextField()),
                ('applicant_signature', models.BooleanField(default=True)),
                ('supervisor_signature', models.BooleanField(default=False)),
                ('accounting_signature', models.BooleanField(default=False)),
                ('total_bills', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total_expense', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_expense_dollars', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='general.area')),
                ('for_interested', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='area_interesada', to='general.area')),
                ('from_interested', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usuario_interesado', to=settings.AUTH_USER_MODEL)),
                ('laboratory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='general.laboratory')),
                ('persons', models.ManyToManyField(related_name='viajantes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceBill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_image', models.ImageField(blank=True, null=True, upload_to='bills/')),
                ('bill_ruc', models.IntegerField()),
                ('bill_emisor', models.CharField(max_length=100)),
                ('bill_number', models.CharField(max_length=50)),
                ('bill_date', models.DateField()),
                ('bill_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bill_details', models.TextField(blank=True, null=True)),
                ('is_active', models.CharField(max_length=50)),
                ('is_found', models.CharField(max_length=50)),
                ('service_bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_bills', to='perdiems.requestservice')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount', models.IntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('items', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_item', to='perdiems.items')),
                ('request_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_items', to='perdiems.requestservice')),
            ],
        ),
    ]