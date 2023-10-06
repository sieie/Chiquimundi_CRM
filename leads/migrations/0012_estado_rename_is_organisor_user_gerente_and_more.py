# Generated by Django 4.1.6 on 2023-09-18 07:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0011_lead_date_added_lead_description_lead_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.RenameField(
            model_name='user',
            old_name='is_organisor',
            new_name='gerente',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='is_agent',
            new_name='vendedor',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='organisation',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='category',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='organisation',
        ),
        migrations.AddField(
            model_name='agent',
            name='apellido',
            field=models.CharField(default='SinApellido', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agent',
            name='cedula',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='agent',
            name='email',
            field=models.EmailField(default='Null', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agent',
            name='fecha_ingreso',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agent',
            name='nombre',
            field=models.CharField(default='Null', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agent',
            name='telefono',
            field=models.CharField(default='Null', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lead',
            name='cedula',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='agent',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AddField(
            model_name='estado',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leads.userprofile'),
        ),
        migrations.AddField(
            model_name='lead',
            name='estado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leads', to='leads.estado'),
        ),
    ]
