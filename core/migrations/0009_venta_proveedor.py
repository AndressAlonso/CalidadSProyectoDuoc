# Generated by Django 5.0.6 on 2024-10-25 00:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_rename_idtipoususario_tipousuario_idtipousuario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='proveedor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='proveedor', to='core.usuario'),
        ),
    ]
