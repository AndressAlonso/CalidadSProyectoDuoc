from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("gestion/producto", GestProducto, name="GestProducto"),
    path("gestion/admin", adminConfig, name="adminConfig"),
    path("Carrito", carro, name="carrito"),
    path("addToCar/<int:id>", addToCar, name="addToCar"),
    path("delToCar/<int:id>/", delToCar, name="delToCar"),
    path("producto/detalle/<int:id>", detalle, name="detalle"),
    path("eliminarProducto/<int:id>", eliminarProducto, name="eliminarProducto"),
]
