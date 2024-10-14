from django.contrib import admin
 
from .models import *
# Register your models here.

admin.site.register(tipoUsuario)
admin.site.register(TipoProducto)
admin.site.register(Producto)
admin.site.register(venta)
admin.site.register(DetalleVenta)
admin.site.register(Usuario)
admin.site.register(TipoSemilla)
admin.site.register(TipoInsumo)
admin.site.register(tipoOrigen)

