from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name="home"),
    path('gestion/Producto', GestProducto, name="TuProducto"),
    path('gestion/Admin', adminConfig, name="adminConfig"),
]
