# Generated by Django 5.0.6 on 2024-10-13 22:43

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoInsumo',
            fields=[
                ('idTipoInsumo', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='tipoOrigen',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TipoProducto',
            fields=[
                ('idTipoProducto', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TipoSemilla',
            fields=[
                ('idTipoSemilla', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='tipoUsuario',
            fields=[
                ('idtipoUsusario', models.AutoField(primary_key=True, serialize=False)),
                ('Tipo', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tipousuario')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(choices=[('semilla', 'Semilla'), ('insumo', 'Insumo')], max_length=10)),
                ('stock', models.IntegerField()),
                ('nombre', models.CharField(max_length=80)),
                ('descripcion', models.CharField(max_length=90)),
                ('precio', models.IntegerField()),
                ('a', models.CharField(max_length=50)),
                ('tipoInsumo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.tipoinsumo')),
                ('origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tipoorigen')),
                ('tipoSemilla', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.tiposemilla')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='venta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField(default=datetime.datetime.now)),
                ('total', models.IntegerField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('precio', models.IntegerField()),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.producto')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.venta')),
            ],
        ),
    ]
