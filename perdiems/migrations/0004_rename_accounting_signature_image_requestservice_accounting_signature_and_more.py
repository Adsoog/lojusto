# Generated by Django 5.1.4 on 2024-12-27 00:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perdiems', '0003_remove_requestservice_accounting_signature_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requestservice',
            old_name='accounting_signature_image',
            new_name='accounting_signature',
        ),
        migrations.RenameField(
            model_name='requestservice',
            old_name='applicant_signature_image',
            new_name='applicant_signature',
        ),
        migrations.RenameField(
            model_name='requestservice',
            old_name='supervisor_signature_image',
            new_name='supervisor_signature',
        ),
    ]
