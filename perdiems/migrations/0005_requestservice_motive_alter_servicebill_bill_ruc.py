# Generated by Django 5.1.4 on 2024-12-30 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perdiems', '0004_rename_accounting_signature_image_requestservice_accounting_signature_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestservice',
            name='motive',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='servicebill',
            name='bill_ruc',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
