# Generated by Django 4.2.1 on 2023-10-03 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0019_rename_fecha_ingreso_proforma_fecha_cotizacion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='proforma',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='proformas/'),
        ),
    ]
