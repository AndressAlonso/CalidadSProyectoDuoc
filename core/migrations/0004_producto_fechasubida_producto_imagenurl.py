# Generated by Django 5.0.6 on 2024-10-13 23:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_a_producto_cantidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='fechasubida',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='producto',
            name='imagenUrl',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
