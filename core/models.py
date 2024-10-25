from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class TipoUsuario(models.Model):
    idtipoUsuario = models.AutoField(primary_key=True)
    tipo = models.CharField(null=True, max_length=50)
    def __str__(self):
        return self.tipo

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE, related_name='usuarios', default=1)

    def __str__(self):
        return self.usuario.username


class TipoProducto(models.Model):
    idTipoProducto = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo


class TipoSemilla(models.Model):
    idTipoSemilla = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=80)  # Ej: "Hortaliza", "Frutal", etc.
    def __str__(self):
        return self.tipo


class TipoInsumo(models.Model):
    idTipoInsumo = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50) 
    def __str__(self):
        return self.tipo


class tipoOrigen(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50)
    def __str__(self):
        return self.tipo

class Producto(models.Model):
    TIPO_CHOICES = [
        ('semilla', 'Semilla'),
        ('insumo', 'Insumo'),
    ]

    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)  # Define si es semilla o insumo
    stock = models.IntegerField()
    nombre = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=250)
    precio = models.IntegerField()
    proveedor = models.ForeignKey(to=Usuario, on_delete=models.CASCADE)
    origen = models.ForeignKey(to=tipoOrigen, on_delete=models.CASCADE)
    cantidad = models.CharField(max_length=50)
    imagenUrl = models.CharField(max_length=1000, default='')
    fechasubida = models.DateField(default=datetime.now)
    tipoSemilla = models.ForeignKey(to=TipoSemilla, null=True, blank=True, on_delete=models.CASCADE)
    tipoInsumo = models.ForeignKey(to=TipoInsumo, null=True, blank=True, on_delete=models.CASCADE)
    cantidadVentas = models.IntegerField(default=0)
    inventario = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(default=datetime.now)
    cliente = models.ForeignKey(to=Usuario, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(to=Usuario, on_delete=models.CASCADE, related_name='proveedor', default=1)
    total = models.IntegerField()
    def __str__(self):
        return self.cliente.usuario.username


class DetalleVenta(models.Model):
    id = models.AutoField(primary_key=True)
    venta = models.ForeignKey(to=Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(to=Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.IntegerField()

    def __str__(self):
        return self.producto.nombre
    

