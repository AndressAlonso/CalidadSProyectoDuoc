# Generated by Django 5.0.6 on 2024-10-20 02:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_producto_inventario'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='tipousuario',
            old_name='idtipoUsusario',
            new_name='idtipoUsuario',
        ),
        migrations.RenameField(
            model_name='tipousuario',
            old_name='Tipo',
            new_name='tipo',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='tipoUsuario',
        ),
        migrations.AddField(
            model_name='usuario',
            name='tipo_usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='usuarios', to='core.tipousuario'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL),
        ),
    ]
