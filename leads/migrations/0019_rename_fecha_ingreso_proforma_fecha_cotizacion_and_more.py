# Generated by Django 4.2.1 on 2023-09-27 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0018_agent_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proforma',
            old_name='fecha_ingreso',
            new_name='fecha_cotizacion',
        ),
        migrations.RemoveField(
            model_name='proforma',
            name='articulo',
        ),
        migrations.AddField(
            model_name='proforma',
            name='articulos',
            field=models.ManyToManyField(to='leads.articulo'),
        ),
    ]
