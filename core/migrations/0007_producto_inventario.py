# Generated by Django 5.0.6 on 2024-10-19 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_producto_cantidadventas'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='inventario',
            field=models.BooleanField(default=False),
        ),
    ]
